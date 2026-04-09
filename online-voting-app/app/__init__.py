# app/__init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import db

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # =======================
    # Basic Config
    # =======================
    app.config['SECRET_KEY'] = 'dev-secret-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # =======================
    # Secure Session Cookies
    # =======================
    app.config.update(
        SESSION_COOKIE_SECURE=True,      # Only over HTTPS
        SESSION_COOKIE_HTTPONLY=True,    # Not accessible by JS
        SESSION_COOKIE_SAMESITE='Lax'    # CSRF protection
    )

    # =======================
    # Initialize DB & CSRF
    # =======================
    db.init_app(app)
    csrf.init_app(app)

    # =======================
    # Security Headers
    # =======================
    @app.after_request
    def add_security_headers(response):
        # General security headers
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'

        # CSP - full coverage including fallbacks
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none'; "
            "frame-src 'none'; "
            "worker-src 'self'; "
            "manifest-src 'self'; "
            "base-uri 'self';"
        )

        # Cross-origin policies
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

        # Hide server version
        response.headers['Server'] = 'SecureServer'

        return response

    # =======================
    # Import Routes & Create DB
    # =======================
    with app.app_context():
        from . import routes
        db.create_all()

    return app
