from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__,
                static_folder="static",
                template_folder="templates")
    # ‑- config ----------------------------------------------------
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///finance.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ‑- extensions -----------------------------------------------
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # ‑- blueprints -----------------------------------------------
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # ‑- create tables --------------------------------------------
    with app.app_context():
        db.create_all()

    return app
