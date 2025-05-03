from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.blood import BloodDonation, BloodRequest
from app.models.user import User
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    stats = {
        'total_donors': User.query.filter(User.role == 'user').count(),
        'available_donations': BloodDonation.query.filter_by(status='available').count(),
        'pending_requests': BloodRequest.query.filter_by(status='pending').count()
    }
    
    # Get available blood by type
    blood_inventory = {}
    for blood_type in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
        count = BloodDonation.query.filter_by(
            blood_type=blood_type, 
            status='available'
        ).count()
        blood_inventory[blood_type] = count
    
    return render_template('main/index.html', 
                         stats=stats, 
                         blood_inventory=blood_inventory)

@bp.route('/dashboard')
@login_required
def dashboard():
    context = {
        'now': datetime.utcnow(),
        'user_stats': {
            'total_donations': 0,
            'pending_requests': 0,
            'approved_requests': 0
        }
    }
    
    if current_user.role == 'admin':
        # Admin dashboard data
        context.update({
            'recent_donations': BloodDonation.query.order_by(
                BloodDonation.donation_date.desc()
            ).limit(5).all(),
            'urgent_requests': BloodRequest.query.filter_by(
                urgency_level='high', 
                status='pending'
            ).order_by(BloodRequest.request_date.desc()).limit(5).all(),
            'blood_inventory': {},
            'expiring_soon': BloodDonation.query.filter_by(
                status='available'
            ).order_by(BloodDonation.expiry_date.asc()).limit(5).all()
        })
        
        # Calculate blood inventory
        for blood_type in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']:
            count = BloodDonation.query.filter_by(
                blood_type=blood_type, 
                status='available'
            ).count()
            context['blood_inventory'][blood_type] = count
    else:
        # Regular user dashboard data
        context.update({
            'recent_donations': BloodDonation.query.filter_by(
                donor_id=current_user.id
            ).order_by(BloodDonation.donation_date.desc()).limit(5).all(),
            'my_requests': BloodRequest.query.filter_by(
                requester_id=current_user.id
            ).order_by(BloodRequest.request_date.desc()).limit(5).all()
        })
        
        # Calculate user statistics
        context['user_stats'].update({
            'total_donations': BloodDonation.query.filter_by(
                donor_id=current_user.id
            ).count(),
            'pending_requests': BloodRequest.query.filter_by(
                requester_id=current_user.id,
                status='pending'
            ).count(),
            'approved_requests': BloodRequest.query.filter_by(
                requester_id=current_user.id,
                status='approved'
            ).count()
        })
    
    return render_template('main/dashboard.html', **context)