from flask import render_template, request, redirect, url_for, session, abort
from app import app, db
from app.models import Ballot

import uuid
import hashlib
import logging
import os

# =========================
# 🔐 LOGGING SETUP
# =========================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("audit_log.txt")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(file_handler)


# =========================
# 🔐 CSRF TOKEN GENERATION
# =========================
@app.before_request
def generate_csrf():
    if "csrf_token" not in session:
        session["csrf_token"] = os.urandom(16).hex()


# =========================
# 🔐 SECURITY HEADERS (FIX ALL ZAP WARNINGS)
# =========================
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'  # Clickjacking
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "frame-ancestors 'none';"
    )

    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Permissions-Policy'] = 'geolocation=(), camera=()'

    return response


# =========================
# 🏠 HOME ROUTE
# =========================
@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())[:8]
    return render_template("vote.html")


# =========================
# 🗳 CAST VOTE (CSRF FIX)
# =========================
@app.route("/cast_vote", methods=["POST"])
def cast_vote():

    # 🔐 CSRF PROTECTION
    token = session.get("csrf_token")
    if not token or token != request.form.get("csrf_token"):
        abort(403)

    user_id = str(session.get("user_id"))
    candidate = request.form.get("candidate")

    if not candidate:
        return "Selection required", 400

    user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:10]

    new_vote = Ballot(user_id=user_id, vote=candidate)
    db.session.add(new_vote)
    db.session.commit()

    logger.info(f"AUDIT: User [Hash: {user_hash}] voted. Ballot ID: {new_vote.id}")

    return redirect(url_for('get_ballot', ballot_id=new_vote.id))


# =========================
# 📄 VIEW BALLOT (IDOR FIX)
# =========================
@app.route("/ballot/<int:ballot_id>")
def get_ballot(ballot_id):
    user_id = session.get("user_id")

    # 🔐 IDOR FIX (STRICT AUTHORIZATION)
    ballot = Ballot.query.filter_by(id=ballot_id, user_id=user_id).first()

    if not ballot:
        abort(403)

    return render_template("thank_you.html", ballot=ballot)
