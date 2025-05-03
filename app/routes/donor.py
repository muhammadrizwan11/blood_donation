from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app import db
from app.models.blood import BloodDonation, BloodRequest
from app.models.user import User
from config import Config

bp = Blueprint('donor', __name__, url_prefix='/donor')

@bp.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    if not current_user.is_available:
        flash('You are not eligible to donate at this time due to recent donation.')
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        # Calculate expiry date (42 days from donation)
        expiry_date = datetime.utcnow() + timedelta(days=Config.BLOOD_EXPIRY_DAYS)
        
        donation = BloodDonation(
            donor_id=current_user.id,
            blood_type=current_user.blood_type,
            quantity_ml=request.form.get('quantity', type=int),
            expiry_date=expiry_date
        )
        
        # Update user's last donation date and availability
        current_user.last_donation = datetime.utcnow()
        current_user.is_available = False
        
        db.session.add(donation)
        db.session.commit()
        
        flash('Thank you for your donation!')
        return redirect(url_for('main.dashboard'))
        
    return render_template('donor/donate.html')

@bp.route('/request-blood', methods=['GET', 'POST'])
@login_required
def request_blood():
    if request.method == 'POST':
        blood_request = BloodRequest(
            requester_id=current_user.id,
            blood_type=request.form['blood_type'],
            quantity_ml=request.form.get('quantity', type=int),
            urgency_level=request.form['urgency'],
            hospital=request.form['hospital'],
            purpose=request.form['purpose']
        )
        
        db.session.add(blood_request)
        db.session.commit()
        
        flash('Blood request submitted successfully!')
        return redirect(url_for('main.dashboard'))
        
    return render_template('donor/request_blood.html')

@bp.route('/my-donations')
@login_required
def my_donations():
    donations = BloodDonation.query.filter_by(
        donor_id=current_user.id
    ).order_by(BloodDonation.donation_date.desc()).all()
    return render_template('donor/my_donations.html', donations=donations)

@bp.route('/my-requests')
@login_required
def my_requests():
    requests = BloodRequest.query.filter_by(
        requester_id=current_user.id
    ).order_by(BloodRequest.request_date.desc()).all()
    return render_template('donor/my_requests.html', requests=requests)