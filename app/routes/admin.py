from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.blood import BloodDonation, BloodRequest
from app.models.user import User

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You need administrative privileges to access this page.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def admin_dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_donations': BloodDonation.query.count(),
        'total_requests': BloodRequest.query.count(),
        'pending_requests': BloodRequest.query.filter_by(status='pending').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@bp.route('/manage-users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@bp.route('/manage-donations')
@login_required
@admin_required
def manage_donations():
    donations = BloodDonation.query.order_by(BloodDonation.donation_date.desc()).all()
    return render_template('admin/manage_donations.html', donations=donations)

@bp.route('/manage-requests')
@login_required
@admin_required
def manage_requests():
    requests = BloodRequest.query.order_by(BloodRequest.request_date.desc()).all()
    return render_template('admin/manage_requests.html', requests=requests)

@bp.route('/update-request/<int:request_id>', methods=['POST'])
@login_required
@admin_required
def update_request(request_id):
    blood_request = BloodRequest.query.get_or_404(request_id)
    action = request.form.get('action')
    
    if action == 'approve':
        # Find matching donation
        matching_donation = BloodDonation.query.filter_by(
            blood_type=blood_request.blood_type,
            status='available'
        ).first()
        
        if matching_donation:
            matching_donation.status = 'used'
            blood_request.status = 'approved'
            blood_request.matched_donation_id = matching_donation.id
            flash('Blood request approved and matched with available donation.')
        else:
            flash('No matching blood donation available.')
    
    elif action == 'reject':
        blood_request.status = 'rejected'
        flash('Blood request rejected.')
    
    db.session.commit()
    return redirect(url_for('admin.manage_requests'))