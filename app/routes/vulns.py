# Vulnerable endpoints: SQLi, XSS, unsafe deserialization, secrets leak
import os
import sqlite3
import pickle
from flask import Blueprint, request, jsonify, render_template_string

bp = Blueprint('vulns', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'demo.db')

# --- DB helper (naive: creates a small users table) ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, secret TEXT)')
    # seed data
    c.execute("INSERT OR IGNORE INTO users (id, username, secret) VALUES (1, 'alice', 'alice_secret')")
    c.execute("INSERT OR IGNORE INTO users (id, username, secret) VALUES (2, 'bob', 'bob_secret')")
    conn.commit()
    conn.close()

init_db()

# --- 1) SQL Injection: dynamically built query (vulnerable) ---
@bp.route('/sqli', methods=['GET'])
def sqli():
    # user controls 'q'
    q = request.args.get('q', '')
    # vulnerable: direct string formatting into SQL
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = f"SELECT id, username, secret FROM users WHERE username = '{q}';"
    # return the raw SQL and the result (makes it obvious in demo)
    try:
        rows = c.execute(sql).fetchall()
    except Exception as e:
        return jsonify({"error": str(e), "sql": sql}), 400
    conn.close()
    return jsonify({"sql": sql, "rows": rows})

# --- 2) Reflected XSS: render unsanitized user input ---
@bp.route('/xss', methods=['GET'])
def xss():
    name = request.args.get('name', '<em>world</em>')
    # render_template_string will render the HTML unsafely
    html = f"<h1>Hello {name}</h1>"
    return render_template_string(html)

# --- 3) Unsafe deserialization (pickle) ---
@bp.route('/unpickle', methods=['POST'])
def unpickle():
    # Accepts raw bytes with Content-Type: application/octet-stream
    data = request.get_data()
    # Vulnerable: blindly unpickles arbitrary data
    try:
        obj = pickle.loads(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"unpickled_type": str(type(obj)), "repr": repr(obj)})

# --- 4) Secret leak endpoint (accidentally exposes config) ---
@bp.route('/secret', methods=['GET'])
def secret():
    # returns internal secret (bad practice)
    return jsonify({"secret": "hardcoded_secret_for_demo"})

