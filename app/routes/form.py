import os, sqlite3
from flask import Blueprint, request, render_template, redirect, url_for, make_response

bp = Blueprint('form', __name__, template_folder="../templates")

DB = os.path.join(os.path.dirname(__file__), '..', 'demo_app.db')

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, name TEXT, message TEXT)')
    conn.commit()
    conn.close()

init_db()

# Index + reflected XSS demo (unsanitized)
@bp.route('/', methods=['GET'])
def index():
    name = request.args.get('name', '')
    # reflected XSS: echo directly
    greeting = f"Hello {name}"
    return render_template("index.html", greeting=greeting)

# Form that stores messages (stored XSS + SQLi)
@bp.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '')
    message = request.form.get('message', '')
    # Vulnerable: direct SQL string building -> SQLi
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    sql = f"INSERT INTO messages (name, message) VALUES ('{name}', '{message}')"
    c.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('form.messages'))

@bp.route('/messages', methods=['GET'])
def messages():
    # fetch messages and render without escaping => stored XSS
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, name, message FROM messages ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("stored_xss.html", rows=rows)

