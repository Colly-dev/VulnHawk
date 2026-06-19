
from flask import Flask
from flask_cors import CORS
from src.database.models import db
from src.database.init_db import init_database
import os

def create_app(config_name='development'):
    """Flask application factory."""
    app = Flask(__name__)
    
    # Configuration
    if config_name == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/secureaudit.db'
        app.config['DEBUG'] = True
    elif config_name == 'production':
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///databases/secureaudit.db')
        app.config['DEBUG'] = False
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Initialize database
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from src.dashboard.routes.overview import overview_bp
    from src.dashboard.routes.audits import audits_bp
    from src.dashboard.routes.compliance import compliance_bp
    from src.dashboard.routes.findings import findings_bp
    from src.dashboard.routes.reports import reports_bp
    from src.dashboard.routes.api import api_bp
    
    app.register_blueprint(overview_bp)
    app.register_blueprint(audits_bp)
    app.register_blueprint(compliance_bp)
    app.register_blueprint(findings_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_bp)
    
    return app
