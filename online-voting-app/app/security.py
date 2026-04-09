from flask import current_app as app

@app.after_request
def add_security_headers(response):
    # Enforce protection as per CDF Unit 5
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"
    return response 