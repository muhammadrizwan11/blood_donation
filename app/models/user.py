from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')
    blood_type = db.Column(db.String(5))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    last_donation = db.Column(db.DateTime)
    is_available = db.Column(db.Boolean, default=True)
    donations = db.relationship('BloodDonation', backref='donor', lazy='dynamic')
    requests = db.relationship('BloodRequest', backref='requester', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)