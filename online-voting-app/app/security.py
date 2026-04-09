from flask import current_app as app

@app.after_request
def add_security_headers(response):

    # ✅ Clickjacking Protection
    response.headers["X-Frame-Options"] = "DENY"

    # ✅ Content Security Policy (FULL FIX)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "frame-ancestors 'none';"
    )

    # ✅ Fix MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # ✅ XSS Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # ✅ Referrer leak protection
    response.headers["Referrer-Policy"] = "no-referrer"

    # ✅ Permissions Policy (fix ZAP warning)
    response.headers["Permissions-Policy"] = "geolocation=(), camera=()"

    return response
