from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import db

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 🔐 Secure session cookie configuration
    app.config.update(
        SESSION_COOKIE_SECURE=True,      # HTTPS only
        SESSION_COOKIE_HTTPONLY=True,    # JS cannot access
        SESSION_COOKIE_SAMESITE='Lax'    # Prevent CSRF
    )

    db.init_app(app)
    csrf.init_app(app)

    # 🔐 Security headers after each request
    @app.after_request
    def add_security_headers(response):
        # Clickjacking protection
        response.headers['X-Frame-Options'] = 'DENY'

        # Prevent MIME sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # Basic XSS filter
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "frame-ancestors 'none';"
        )

        # Referrer policy
        response.headers['Referrer-Policy'] = 'no-referrer'

        # Permissions policy
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=()'

        # Cross-Origin Resource Policy
        response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

        # Hide Flask/Werkzeug version
        response.headers['Server'] = 'SecureServer'

        return response

    with app.app_context():
        from . import routes
        db.create_all()

    return app
