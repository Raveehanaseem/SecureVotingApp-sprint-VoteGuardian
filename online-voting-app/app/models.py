from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ballot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    vote = db.Column(db.String(100), nullable=False)