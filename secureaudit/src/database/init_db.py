
from .models import db, Audit, Finding, Report, ComplianceResult

def init_database(app):
    """Initialize the database with the Flask app."""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")

def reset_database(app):
    """Reset the database (drop all tables and recreate)."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset successfully.")
