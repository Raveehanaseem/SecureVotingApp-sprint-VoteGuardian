from flask import Flask, g
from flask_wtf.csrf import CSRFProtect
from .models import db
import secrets

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Basic config
    app.config['SECRET_KEY'] = 'dev-secret-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Secure session cookies
    # FIX [90027] Cookie Slack Detector:
    # SESSION_COOKIE_SECURE, HTTPONLY, SAMESITE='Strict' tightens cookie policy.
    # Using 'Strict' instead of 'Lax' prevents any cross-site cookie leakage.
    app.config.update(
        SESSION_COOKIE_SECURE=True,       # Only over HTTPS
        SESSION_COOKIE_HTTPONLY=True,     # Not accessible via JS
        SESSION_COOKIE_SAMESITE='Strict'  # Strictest CSRF cookie protection
    )

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # Security headers
    @app.before_request
    def generate_nonce():
        # FIX [10055] CSP unsafe-inline: Generate a per-request nonce for inline styles.
        # This nonce is injected into CSP and into every template via g.csp_nonce.
        g.csp_nonce = secrets.token_hex(16)

    @app.after_request
    def add_security_headers(response):
        nonce = getattr(g, 'csp_nonce', secrets.token_hex(16))

        # General security headers
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=()'

        # FIX [10055] CSP: style-src unsafe-inline [10055]:
        # Replace 'unsafe-inline' with a per-request nonce.
        # Templates must use <style nonce="{{ g.csp_nonce }}"> for inline styles.
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self'; "
            f"style-src 'self' 'nonce-{nonce}'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )

        # Cross-origin policies
        response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
        response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
        response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'

        # FIX [10036] Server Leaks Version Information:
        # Override the Server header so Werkzeug version is never exposed.
        response.headers['Server'] = 'SecureServer'

        return response

    # Import routes and create database
    with app.app_context():
        from . import routes
        db.create_all()

    return app
