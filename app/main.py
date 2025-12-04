from flask import Flask
from app.routes.form import bp as form_bp
from app.routes.auth import bp as auth_bp
from app.routes.upload import bp as upload_bp
from app.routes.vulns_all import bp as vulns_bp

def create_app():
    app = Flask(__name__)
    # intentionally insecure: hardcoded secret, debug True
    app.config.update(
        SECRET_KEY = "HARD_CODED_SECRET_DEMO",
        DEBUG = True,
        SESSION_COOKIE_SECURE = False,   # insecure for demo
        SESSION_COOKIE_HTTPONLY = False, # insecure for demo
    )

    app.register_blueprint(form_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(vulns_bp, url_prefix='/vuln' ) 
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)

