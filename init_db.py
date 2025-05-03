from app import create_app, db
from app.models.user import User
from datetime import datetime

def init_db():
    app = create_app()
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@blooddonation.com',
                role='admin',
                blood_type='O+',
                phone='1234567890',
                address='Blood Bank Main Office',
                is_available=False
            )
            admin.set_password('admin123')  # Change this password in production
            db.session.add(admin)
            db.session.commit()
            print('Admin user created successfully!')
        else:
            print('Admin user already exists.')

if __name__ == '__main__':
    init_db()