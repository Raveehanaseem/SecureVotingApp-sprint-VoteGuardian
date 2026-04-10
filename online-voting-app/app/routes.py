from flask import render_template, request, session, redirect, url_for, abort, current_app as app
from .models import Ballot, db
import hashlib
import uuid
import logging

# ----------------------------
# Logging Configuration
# ----------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler for audit logs
file_handler = logging.FileHandler("audit_log.txt")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(file_handler)

# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def index():
    # Assign a unique session ID if none exists
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())[:8]
    return render_template("vote.html")

@app.route("/cast_vote", methods=["POST"])
def cast_vote():
    user_id = session.get("user_id")
    candidate = request.form.get("candidate")

    # Validation
    if not user_id or not candidate:
        return "Invalid session or selection required", 400

    # Hash user ID for logging
    user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:10]

    # Store vote
    new_vote = Ballot(user_id=user_id, vote=candidate)
    db.session.add(new_vote)
    db.session.commit()

    # Audit log
    logger.info(f"AUDIT: User [Hash: {user_hash}] cast vote. Ballot ID: {new_vote.id}")

    return redirect(url_for('get_ballot', ballot_id=new_vote.id))

@app.route("/ballot/<int:ballot_id>")
def get_ballot(ballot_id):
    user_id = session.get("user_id")

    # Only allow the user who created the ballot to view it
    ballot = Ballot.query.filter_by(id=ballot_id, user_id=user_id).first()
    if not ballot:
        abort(403)  # Forbidden

    return render_template("thank_you.html", ballot=ballot)

