from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .models import db

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app