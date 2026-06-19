
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Audit(db.Model):
    __tablename__ = 'audits'
    
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255), nullable=False)
    audit_type = db.Column(db.String(50), nullable=False)  # web, cloud, os, network
    status = db.Column(db.String(20), default='completed')  # completed, in_progress, failed
    score = db.Column(db.Float, default=0.0)
    rating = db.Column(db.String(20))  # Excellent, Good, Fair, Poor, Critical
    total_findings = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    findings = db.relationship('Finding', backref='audit', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'target': self.target,
            'audit_type': self.audit_type,
            'status': self.status,
            'score': self.score,
            'rating': self.rating,
            'total_findings': self.total_findings,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Finding(db.Model):
    __tablename__ = 'findings'
    
    id = db.Column(db.Integer, primary_key=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
    finding_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    finding_type = db.Column(db.String(100))
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'audit_id': self.audit_id,
            'finding_id': self.finding_id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'type': self.finding_type,
            'category': self.category,
            'created_at': self.created_at.isoformat()
        }

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # executive, technical, compliance, remediation
    format = db.Column(db.String(20), default='html')  # html, json, csv, pdf
    content = db.Column(db.LargeBinary)
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'audit_id': self.audit_id,
            'report_type': self.report_type,
            'format': self.format,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat()
        }

class ComplianceResult(db.Model):
    __tablename__ = 'compliance_results'
    
    id = db.Column(db.Integer, primary_key=True)
    audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
    benchmark = db.Column(db.String(100), nullable=False)  # CIS Linux, CIS AWS, etc.
    score = db.Column(db.Float)
    passed = db.Column(db.Integer)
    failed = db.Column(db.Integer)
    total = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'audit_id': self.audit_id,
            'benchmark': self.benchmark,
            'score': self.score,
            'passed': self.passed,
            'failed': self.failed,
            'total': self.total,
            'created_at': self.created_at.isoformat()
        }
