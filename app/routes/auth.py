from flask import Blueprint, request, redirect, url_for, make_response, render_template

bp = Blueprint('auth', __name__, template_folder="../templates")

# Very simple insecure login for demo
USERS = {"alice":"password123", "bob":"qwerty"}

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    username = request.form.get('username')
    pwd = request.form.get('password')
    if USERS.get(username) == pwd:
        # insecure cookie: no HttpOnly, no Secure, signed with hardcoded secret above
        resp = make_response(redirect('/'))
        resp.set_cookie('demo_auth', f"{username}|token", httponly=False, secure=False)
        return resp
    return "Invalid", 401

@bp.route('/profile')
def profile():
    cookie = request.cookies.get('demo_auth')
    if not cookie:
        return redirect(url_for('auth.login'))
    user = cookie.split('|')[0]
    return f"Profile page of {user}"

