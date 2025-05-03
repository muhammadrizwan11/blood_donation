from app import db
from datetime import datetime

class BloodDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    quantity_ml = db.Column(db.Integer, nullable=False)
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='available')
    expiry_date = db.Column(db.DateTime, nullable=False)

class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blood_type = db.Column(db.String(5), nullable=False)
    quantity_ml = db.Column(db.Integer, nullable=False)
    urgency_level = db.Column(db.String(20), default='normal')
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    hospital = db.Column(db.String(200))
    purpose = db.Column(db.Text)
    matched_donation_id = db.Column(db.Integer, db.ForeignKey('blood_donation.id'))