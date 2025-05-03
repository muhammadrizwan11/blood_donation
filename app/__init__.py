from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
migrate = Migrate()
bootstrap = Bootstrap5()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # Register blueprints
    from app.routes import main, auth, donor, admin
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(donor.bp)
    app.register_blueprint(admin.bp)

    return app

from app.models import user, blood