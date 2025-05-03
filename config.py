import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///blood_donation.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Blood donation specific settings
    BLOOD_EXPIRY_DAYS = 42  # Blood typically expires after 42 days
    MINIMUM_DONATION_ML = 350  # Minimum donation amount in milliliters
    MAXIMUM_DONATION_ML = 500  # Maximum donation amount in milliliters
    
    # Donation interval (minimum time between donations)
    MALE_DONATION_INTERVAL = timedelta(days=84)    # 12 weeks for males
    FEMALE_DONATION_INTERVAL = timedelta(days=112)  # 16 weeks for females