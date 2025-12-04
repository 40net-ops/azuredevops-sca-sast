# app/routes/vulns_all.py
# Vulnerable demo endpoints (for lab only)
import os
import sqlite3
import pickle
import subprocess
import hashlib
import xml.etree.ElementTree as ET   # used to demonstrate XXE if misused
import requests
from flask import Blueprint, request, jsonify, render_template_string, redirect, send_from_directory

bp = Blueprint("vulns_all", __name__)

# --- Setup a small DB for SQLi / stored XSS / IDOR demos ---
DB = os.path.join(os.path.dirname(__file__), "..", "vulns_all.db")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, is_admin INTEGER, secret TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, owner_id INTEGER, note TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, name TEXT, message TEXT)')
    # seed
    c.execute("INSERT OR IGNORE INTO users (id, username, is_admin, secret) VALUES (1, 'alice', 1, 'alice_secret')")
    c.execute("INSERT OR IGNORE INTO users (id, username, is_admin, secret) VALUES (2, 'bob', 0, 'bob_secret')")
    conn.commit()
    conn.close()

init_db()

# ------------------------------------------------------
# CWE-79 Reflected XSS (reflected)
# - returns user input directly in the HTML without escaping
# ------------------------------------------------------
@bp.route("/xss/reflected", methods=["GET"])
def xss_reflected():
    name = request.args.get("name", "")
    # vulnerable: inserting unsanitized user input into HTML
    html = f"<html><body><h1>Welcome {name}</h1></body></html>"
    return html

# ------------------------------------------------------
# CWE-79 Stored XSS and CWE-89 SQL Injection (stored)
# - store messages (no parameterized queries), then render without escaping
# ------------------------------------------------------
@bp.route("/xss/stored/submit", methods=["POST"])
def xss_stored_submit():
    name = request.form.get("name", "")
    message = request.form.get("message", "")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Vulnerable: direct string formatting -> SQL Injection
    sql = f"INSERT INTO messages (name, message) VALUES ('{name}', '{message}')"
    c.execute(sql)
    conn.commit()
    conn.close()
    return redirect("/xss/stored/list")

@bp.route("/xss/stored/list", methods=["GET"])
def xss_stored_list():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, name, message FROM messages ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    # Vulnerable: rendering messages with |safe like behavior (we use render_template_string)
    items = "".join([f"<div><b>{r[1]}</b>: {r[2]}</div>" for r in rows])
    return f"<html><body><h1>Messages</h1>{items}</body></html>"

# ------------------------------------------------------
# CWE-352 CSRF
# - example of a state-changing endpoint without CSRF protection
# ------------------------------------------------------
@bp.route("/account/delete", methods=["POST"])
def account_delete():
    # No CSRF token validation present -> vulnerable
    user_id = request.form.get("user_id")
    # perform deletion (insecure demo)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(f"DELETE FROM users WHERE id = {user_id}")
    conn.commit()
    conn.close()
    return jsonify({"deleted_user": user_id})

# ------------------------------------------------------
# CWE-22 Path Traversal
# - serve files from uploads folder with no path sanitization
# ------------------------------------------------------
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads_vulns_all")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@bp.route("/file/upload", methods=["POST"])
def file_upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no file"}), 400
    # vulnerable: allow arbitrary filename (directory traversal)
    filename = f.filename
    f.save(os.path.join(UPLOAD_DIR, filename))
    return jsonify({"saved": filename})

@bp.route("/file/get/<path:filename>", methods=["GET"])
def file_get(filename):
    # vulnerable: no sanitization
    return send_from_directory(UPLOAD_DIR, filename)

# ------------------------------------------------------
# CWE-78 OS Command Injection
# - executes user-controlled input in a shell (dangerous)
# ------------------------------------------------------
@bp.route("/cmd/exec", methods=["GET"])
def cmd_exec():
    cmd = request.args.get("cmd", "echo hello")
    # Vulnerable: using shell=True with untrusted input
    result = subprocess.getoutput(cmd)
    return jsonify({"cmd": cmd, "output": result})

# ------------------------------------------------------
# CWE-502 Insecure Deserialization
# - unpickles arbitrary data
# ------------------------------------------------------
@bp.route("/deserialize", methods=["POST"])
def insecure_deserialize():
    data = request.get_data()
    # Vulnerable: pickle.loads on untrusted input
    obj = pickle.loads(data)
    return jsonify({"type": str(type(obj)), "repr": repr(obj)})

# ------------------------------------------------------
# CWE-918 SSRF
# - fetches arbitrary URLs without allow list
# ------------------------------------------------------
@bp.route("/fetch", methods=["GET"])
def fetch_url():
    url = request.args.get("url")
    try:
        r = requests.get(url, timeout=5)
        return (r.text[:1000], r.status_code)   # limit returned size for demo
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------------------------------
# CWE-601 Open Redirect
# - redirect to user-provided URL without validation
# ------------------------------------------------------
@bp.route("/redirect", methods=["GET"])
def open_redirect():
    nxt = request.args.get("next", "/")
    return redirect(nxt)

# ------------------------------------------------------
# CWE-611 XXE (XML External Entity)
# - naive XML parsing using ElementTree (demonstration only)
# ------------------------------------------------------
@bp.route("/xml/parse", methods=["POST"])
def xml_parse():
    data = request.data.decode('utf-8', errors='ignore')
    # Vulnerable usage example: parsing XML without disabling ENTITY resolution in certain parsers
    # Note: xml.etree.ElementTree by default does not process external entities, but some libs do.
    try:
        root = ET.fromstring(data)
        return jsonify({"root_tag": root.tag})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ------------------------------------------------------
# CWE-94 Code Injection (eval)
# - evaluate user expression (unsafe)
# ------------------------------------------------------
@bp.route("/eval", methods=["POST"])
def code_eval():
    expr = request.form.get("expr", "")
    # Vulnerable: direct eval of user input
    result = eval(expr)
    return jsonify({"expr": expr, "result": repr(result)})

# ------------------------------------------------------
# CWE-434 Unrestricted File Upload (no validation)
# - allowed in file_upload above; also show a dedicated endpoint checking extension (missing)
# ------------------------------------------------------
@bp.route("/upload/no_check", methods=["POST"])
def upload_no_check():
    f = request.files.get("file")
    if not f:
        return jsonify({"error":"no file"}), 400
    f.save(os.path.join(UPLOAD_DIR, f.filename))
    return jsonify({"saved": f.filename})

# ------------------------------------------------------
# CWE-327 Weak Cryptography usage
# - demonstrates MD5 hashing for passwords (insecure)
# ------------------------------------------------------
@bp.route("/weakhash", methods=["POST"])
def weak_hash():
    pwd = request.form.get("password", "")
    # Vulnerable: usage of MD5 for password hashing
    h = hashlib.md5(pwd.encode()).hexdigest()
    return jsonify({"md5": h})

# ------------------------------------------------------
# CWE-200 Information Exposure
# - returns internal config / secrets (hardcoded)
# ------------------------------------------------------
HARD_SECRET = "SUPER_SECRET_DEMO"  # CWE-798 / CWE-200
@bp.route("/internal/secret", methods=["GET"])
def internal_secret():
    # vulnerable: exposing secret in endpoint
    return jsonify({"secret": HARD_SECRET})

# ------------------------------------------------------
# CWE-284 Broken Access Control / IDOR (CWE-639)
# - endpoint that allows reading other user's notes via provided id without auth check
# ------------------------------------------------------
@bp.route("/notes/get", methods=["GET"])
def notes_get():
    note_id = request.args.get("id")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # vulnerable: direct id-based access without ownership/auth checks
    c.execute(f"SELECT id, owner_id, note FROM notes WHERE id = {note_id}")
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify({"note": row})

# ------------------------------------------------------
# CWE-668 Insecure CORS (expose resources to any origin)
# - a route that returns CORS header allowing all origins
# ------------------------------------------------------
@bp.route("/cors/open", methods=["GET"])
def cors_open():
    resp = jsonify({"status": "CORS open to all origins"})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

# ------------------------------------------------------
# CWE-306 Missing Authentication
# - a sensitive action endpoint that does not verify the user
# ------------------------------------------------------
@bp.route("/sensitive/action", methods=["POST"])
def sensitive_action():
    # No auth check; performs a "sensitive" action
    return jsonify({"status": "performed sensitive action (no auth)"})


# ------------------------------------------------------
# additional helper: endpoint listing to help discover in demos
@bp.route("/", methods=["GET"])
def index():
    # Return a simple list of endpoints (for demo convenience)
    eps = [rule.rule for rule in bp.url_map.iter_rules()] if hasattr(bp, "url_map") else [
        "/xss/reflected", "/xss/stored/submit", "/xss/stored/list", "/account/delete",
        "/file/upload", "/file/get/<filename>", "/cmd/exec", "/deserialize",
        "/fetch", "/redirect", "/xml/parse", "/eval", "/upload/no_check",
        "/weakhash", "/internal/secret", "/notes/get", "/cors/open", "/sensitive/action"
    ]
    return jsonify({"endpoints_sample": eps})

