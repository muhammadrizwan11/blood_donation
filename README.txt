Blood Donation Management System
============================

A comprehensive web-based system for managing blood donations, requests, and inventory.

Features
--------
1. User Management
   - User registration and authentication
   - Role-based access (Admin/Donor)
   - Profile management
   - Secure password handling

2. Donor Features
   - Submit blood donations
   - Track donation history
   - Request blood
   - View request status
   - Personal dashboard
   - Donation eligibility tracking

3. Administrator Features
   - Manage users
   - Monitor blood inventory
   - Process blood requests
   - Track donations
   - View system statistics
   - Generate reports

4. Blood Management
   - Blood type tracking
   - Expiry date monitoring (42 days)
   - Inventory management
   - Request matching
   - Usage tracking

Technical Specifications
----------------------
- Framework: Flask (Python)
- Database: SQLite with SQLAlchemy ORM
- Frontend: Bootstrap 5
- Authentication: Flask-Login
- Forms: Flask-WTF
- Email: Flask-Mail

System Requirements
-----------------
- Python 3.x
- pip package manager
- Virtual environment
- Modern web browser
- Internet connection

Security Features
---------------
- Password hashing
- Session management
- CSRF protection
- Role-based access control
- Form validation

Database Structure
----------------
1. Users Table
   - Basic information
   - Authentication details
   - Role management
   - Donation history

2. Blood Donations Table
   - Donation records
   - Blood type information
   - Expiry tracking
   - Status management

3. Blood Requests Table
   - Request details
   - Priority management
   - Status tracking
   - Request-donation matching

Business Rules
------------
1. Donation Rules
   - Minimum interval between donations
   - Blood expiry period (42 days)
   - Minimum/maximum donation quantities
   - Donor eligibility tracking

2. Request Processing
   - Priority-based processing
   - Blood type compatibility
   - Inventory checking
   - Request matching

Contact
-------
For support and queries, please contact:
Email: support@blooddonation.com
Phone: +1-XXX-XXX-XXXX

License
-------
Copyright © 2025 Blood Donation System
All rights reserved.