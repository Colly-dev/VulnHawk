
from flask import Blueprint, render_template
from src.database.models import Report, Audit

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
def list_reports():
    """List all reports."""
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template('reports/executive.html', reports=reports)

@reports_bp.route('/<int:report_id>')
def view_report(report_id):
    """View a specific report."""
    report = Report.query.get_or_404(report_id)
    return render_template('reports/executive.html', report=report)
