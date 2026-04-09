import logging
import hashlib
import uuid
from flask import render_template, request, session, redirect, url_for, abort, current_app as app
from .models import Ballot, db

class AuditFilter(logging.Filter):
    def filter(self, record):
        return "AUDIT" in record.getMessage()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)

file_handler = logging.FileHandler("audit_log.txt")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
file_handler.addFilter(AuditFilter()) 
logger.addHandler(file_handler)

logging.getLogger('werkzeug').addHandler(stream_handler)

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())[:8]
    return render_template("vote.html")

@app.route("/cast_vote", methods=["POST"])
def cast_vote():
    user_id = str(session.get("user_id"))
    candidate = request.form.get("candidate")
    
    if not candidate:
        return "Selection required", 400

    user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:10]

    new_vote = Ballot(user_id=user_id, vote=candidate)
    db.session.add(new_vote)
    db.session.commit()

    logger.info(f"AUDIT: User [Hash: {user_hash}] has cast a vote for CR Election. Ballot ID: {new_vote.id}")
    
    return redirect(url_for('get_ballot', ballot_id=new_vote.id))

@app.route("/ballot/<int:ballot_id>")
def get_ballot(ballot_id):
    user_id = session.get("user_id")
    ballot = Ballot.query.filter_by(id=ballot_id, user_id=user_id).first()
    
    if not ballot:
        abort(403)
        
    return render_template("thank_you.html", ballot=ballot)