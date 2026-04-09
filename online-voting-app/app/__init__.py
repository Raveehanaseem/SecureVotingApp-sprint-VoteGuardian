import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import db

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Secret key
    app.config['SECRET_KEY'] = 'dev-secret-key-12345'

    # Secure session cookies
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # SQLite DB inside instance folder (absolute path)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'voting.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    csrf.init_app(app)

    # Security headers and CSP
    @app.after_request
    def add_security_headers(response):
        # General security headers
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=()'

        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none';"
        )

        # Cross-origin policies
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

        # Hide server version
        response.headers['Server'] = 'SecureServer'

        return response

    # Import routes and create DB
    with app.app_context():
        from . import routes
        db.create_all()  # Will now create voting.db in instance folder

    return app
