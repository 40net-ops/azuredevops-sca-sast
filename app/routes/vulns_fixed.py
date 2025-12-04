import os
import sqlite3
import pickle
from flask import Blueprint, request, jsonify, render_template
from markupsafe import escape

bp = Blueprint('vulns_fixed', __name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'demo_fixed.db')

# safer DB init
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, secret TEXT)')
    c.execute("INSERT OR IGNORE INTO users (id, username, secret) VALUES (1, 'alice', 'alice_secret')")
    c.execute("INSERT OR IGNORE INTO users (id, username, secret) VALUES (2, 'bob', 'bob_secret')")
    conn.commit()
    conn.close()

init_db()

# 1) Parameterized query
@bp.route('/sqli', methods=['GET'])
def sqli():
    q = request.args.get('q', '')
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, secret FROM users WHERE username = ?", (q,))
    rows = c.fetchall()
    conn.close()
    return jsonify({"rows": rows})

# 2) XSS: escape output properly
@bp.route('/xss', methods=['GET'])
def xss():
    name = request.args.get('name', 'world')
    # use escape to avoid XSS
    return render_template("safe_hello.html", name=escape(name))

# 3) Safe deserialization policy: reject binary pickle; accept JSON only
@bp.route('/unpickle', methods=['POST'])
def unpickle():
    # refuse pickle content
    if request.content_type == 'application/octet-stream':
        return jsonify({"error": "binary pickle not allowed"}), 400
    # only accept JSON
    try:
        obj = request.get_json(force=True)
    except Exception as e:
        return jsonify({"error": "invalid JSON"}), 400
    return jsonify({"type": str(type(obj)), "repr": repr(obj)})

# 4) Do not expose internal secrets
@bp.route('/secret', methods=['GET'])
def secret():
    return jsonify({"secret": "REDACTED"})  # not returning internal config

