
from flask import Blueprint, render_template, request, redirect, url_for
from src.database.models import db, Audit, Finding

audits_bp = Blueprint('audits', __name__, url_prefix='/audits')

@audits_bp.route('/')
def list_audits():
    """List all audits."""
    page = request.args.get('page', 1, type=int)
    audits = Audit.query.order_by(Audit.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('audits/audit_history.html', audits=audits)

@audits_bp.route('/<int:audit_id>')
def view_audit(audit_id):
    """View a specific audit."""
    audit = Audit.query.get_or_404(audit_id)
    findings = Finding.query.filter_by(audit_id=audit_id).all()
    return render_template('audits/audit_detail.html', audit=audit, findings=findings)

@audits_bp.route('/new')
def new_audit():
    """Create a new audit."""
    return render_template('audits/new_audit.html')
