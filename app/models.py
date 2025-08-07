from . import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id       = db.Column(db.Integer, primary_key=True)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    @staticmethod
    def create(email, plaintext_pw):
        hashed = bcrypt.generate_password_hash(plaintext_pw).decode()
        user = User(email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        return user

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

class Expense(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date        = db.Column(db.Date, nullable=False)
    category    = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    amount      = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='expenses')
