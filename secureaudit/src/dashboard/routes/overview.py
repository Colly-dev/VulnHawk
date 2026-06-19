
from flask import Blueprint, render_template
from src.database.models import Audit, Finding, ComplianceResult

overview_bp = Blueprint('overview', __name__, url_prefix='/')

@overview_bp.route('/')
def dashboard():
    """Main dashboard overview."""
    total_audits = Audit.query.count()
    total_findings = Finding.query.count()
    avg_score = 0
    
    audits = Audit.query.all()
    if audits:
        avg_score = sum(a.score for a in audits) / len(audits)
    
    recent_audits = Audit.query.order_by(Audit.created_at.desc()).limit(5).all()
    
    return render_template('overview.html', 
                         total_audits=total_audits,
                         total_findings=total_findings,
                         avg_score=round(avg_score, 2),
                         recent_audits=recent_audits)
