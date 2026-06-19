
from flask import Blueprint, render_template, request
from src.database.models import Finding

findings_bp = Blueprint('findings', __name__, url_prefix='/findings')

@findings_bp.route('/')
def list_findings():
    """List all findings."""
    severity = request.args.get('severity', None)
    category = request.args.get('category', None)
    
    query = Finding.query
    if severity:
        query = query.filter_by(severity=severity)
    if category:
        query = query.filter_by(category=category)
    
    findings = query.order_by(Finding.created_at.desc()).all()
    return render_template('findings/list.html', findings=findings)
