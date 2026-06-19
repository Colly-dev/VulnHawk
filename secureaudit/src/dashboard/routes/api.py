
from flask import Blueprint, jsonify, request
from src.database.models import db, Audit, Finding, ComplianceResult

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/audits', methods=['GET'])
def get_audits():
    """Get all audits as JSON."""
    audits = Audit.query.all()
    return jsonify([a.to_dict() for a in audits])

@api_bp.route('/audits/<int:audit_id>', methods=['GET'])
def get_audit(audit_id):
    """Get a specific audit."""
    audit = Audit.query.get_or_404(audit_id)
    return jsonify(audit.to_dict())

@api_bp.route('/audits/<int:audit_id>/findings', methods=['GET'])
def get_audit_findings(audit_id):
    """Get findings for a specific audit."""
    findings = Finding.query.filter_by(audit_id=audit_id).all()
    return jsonify([f.to_dict() for f in findings])

@api_bp.route('/findings', methods=['GET'])
def get_findings():
    """Get all findings."""
    findings = Finding.query.all()
    return jsonify([f.to_dict() for f in findings])

@api_bp.route('/compliance', methods=['GET'])
def get_compliance():
    """Get compliance results."""
    results = ComplianceResult.query.all()
    return jsonify([r.to_dict() for r in results])

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics."""
    total_audits = Audit.query.count()
    total_findings = Finding.query.count()
    avg_score = 0
    
    audits = Audit.query.all()
    if audits:
        avg_score = sum(a.score for a in audits) / len(audits)
    
    severity_counts = {}
    for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
        severity_counts[severity] = Finding.query.filter_by(severity=severity).count()
    
    return jsonify({
        'total_audits': total_audits,
        'total_findings': total_findings,
        'avg_score': round(avg_score, 2),
        'severity_counts': severity_counts
    })
