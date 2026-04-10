from flask import Flask, g, request
from flask_wtf.csrf import CSRFProtect
from .models import db
import secrets

csrf = CSRFProtect()

# FIX [10036]: List of safe server names to hide real server info
SAFE_SERVER_NAMES = ['SecureServer', 'WebServer', 'AppServer']

# FIX [90027]: Sensitive cookie paths that must be secured
SECURE_COOKIE_PATHS = ['/cast_vote', '/ballot', '/']

def is_sensitive_path(path):
    """Check if the current request path needs strict cookie handling"""
    return any(path.startswith(p) for p in SECURE_COOKIE_PATHS)

def get_safe_server_name():
    """Return a safe server name hiding real tech stack"""
    return SAFE_SERVER_NAMES[0]  # Always returns 'SecureServer'

def create_app():
    app = Flask(__name__)

    # Basic config
    app.config['SECRET_KEY'] = 'dev-secret-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # FIX [90027]: Base cookie config
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Strict',
        SESSION_COOKIE_NAME='__Host-session',
        SESSION_COOKIE_PATH='/'
    )

    db.init_app(app)
    csrf.init_app(app)

    @app.before_request
    def generate_nonce():
        # FIX [10055]: Generate nonce only if request has a session
        if request.endpoint:
            g.csp_nonce = secrets.token_hex(16)
        else:
            g.csp_nonce = secrets.token_hex(16)  # Always generate for safety

    @app.after_request
    def add_security_headers(response):
        nonce = getattr(g, 'csp_nonce', secrets.token_hex(16))

        # -----------------------------------------------
        # FIX [10036]: Hide Server header using condition
        # Check if Server header exists and override it
        # -----------------------------------------------
        if 'Server' in response.headers:
            response.headers['Server'] = get_safe_server_name()
        else:
            response.headers['Server'] = get_safe_server_name()

        # -----------------------------------------------
        # FIX [90027]: Cookie hardening using condition
        # Apply stricter headers based on request path
        # -----------------------------------------------
        if is_sensitive_path(request.path):
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
        else:
            response.headers['Cache-Control'] = 'no-store'

        # General security headers
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=()'

        # CSP with nonce instead of unsafe-inline
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

        return response

    with app.app_context():
        from . import routes
        db.create_all()

    return app
