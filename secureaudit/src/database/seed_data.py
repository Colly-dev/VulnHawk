
from .models import db, Audit, Finding, ComplianceResult
from datetime import datetime

def seed_demo_data(app):
    """Populate the database with demo audit data."""
    with app.app_context():
        # Check if data already exists
        if Audit.query.first():
            print("Demo data already exists. Skipping seed.")
            return
        
        # Create sample audit
        audit = Audit(
            target="example.com",
            audit_type="web",
            status="completed",
            score=72.5,
            rating="Good",
            total_findings=5
        )
        db.session.add(audit)
        db.session.commit()
        
        # Add sample findings
        findings = [
            Finding(
                audit_id=audit.id,
                finding_id="WEB_HEADER_HSTS",
                title="Missing HSTS Header",
                description="The HTTP Strict-Transport-Security header is not present.",
                severity="HIGH",
                finding_type="MISSING_HSTS",
                category="Web Security"
            ),
            Finding(
                audit_id=audit.id,
                finding_id="TLS_WEAK_PROTOCOL",
                title="Weak TLS Protocol Supported",
                description="The server supports TLS 1.1, which is deprecated.",
                severity="MEDIUM",
                finding_type="WEAK_TLS_PROTOCOL",
                category="TLS/SSL"
            ),
            Finding(
                audit_id=audit.id,
                finding_id="WEB_HEADER_CSP",
                title="Missing Content-Security-Policy Header",
                description="The CSP header is not configured.",
                severity="HIGH",
                finding_type="MISSING_CSP",
                category="Web Security"
            ),
            Finding(
                audit_id=audit.id,
                finding_id="WEB_HEADER_XFO",
                title="Missing X-Frame-Options Header",
                description="Clickjacking protection is not enabled.",
                severity="MEDIUM",
                finding_type="MISSING_XFO",
                category="Web Security"
            ),
            Finding(
                audit_id=audit.id,
                finding_id="WEB_HEADER_XCTO",
                title="Missing X-Content-Type-Options Header",
                description="MIME type sniffing protection is not enabled.",
                severity="LOW",
                finding_type="MISSING_XCTO",
                category="Web Security"
            )
        ]
        
        for finding in findings:
            db.session.add(finding)
        
        db.session.commit()
        
        # Add sample compliance result
        compliance = ComplianceResult(
            audit_id=audit.id,
            benchmark="CIS Linux Benchmark",
            score=65.0,
            passed=13,
            failed=7,
            total=20
        )
        db.session.add(compliance)
        db.session.commit()
        
        print("Demo data seeded successfully.")
