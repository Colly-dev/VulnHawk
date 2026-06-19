
from typing import List, Dict, Any

class RecommendationEngine:
    """
    Generates hardening recommendations based on audit findings.
    """
    
    # Simple knowledge base of remediation steps
    REMEDIATION_KB = {
        "MISSING_HSTS": {
            "title": "Enable HTTP Strict Transport Security (HSTS)",
            "description": "HSTS protects websites against man-in-the-middle attacks such as protocol downgrade attacks and cookie hijacking.",
            "fix_steps": [
                "Configure your web server to send the Strict-Transport-Security header.",
                "Example for Nginx: add_header Strict-Transport-Security 'max-age=31536000; includeSubDomains' always;",
                "Example for Apache: Header always set Strict-Transport-Security 'max-age=31536000; includeSubDomains'"
            ],
            "reference": "https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html"
        },
        "WEAK_TLS_PROTOCOL": {
            "title": "Disable Weak TLS Protocols",
            "description": "Old TLS versions (SSLv2, SSLv3, TLS 1.0, TLS 1.1) are vulnerable to various attacks.",
            "fix_steps": [
                "Disable SSLv2, SSLv3, TLS 1.0, and TLS 1.1 on the server.",
                "Enable TLS 1.2 and TLS 1.3 only.",
                "For Nginx: ssl_protocols TLSv1.2 TLSv1.3;"
            ],
            "reference": "https://ssllabs.com"
        },
        "S3_PUBLIC_ACCESS": {
            "title": "Restrict S3 Public Access",
            "description": "S3 buckets should not be publicly accessible unless explicitly required.",
            "fix_steps": [
                "Enable 'Block all public access' at the bucket level or account level.",
                "Review bucket policies and ACLs for 'AllUsers' or 'AuthenticatedUsers' permissions."
            ],
            "reference": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html"
        }
        # Add more mappings as needed
    }

    @staticmethod
    def generate(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        recommendations = []
        for finding in findings:
            finding_type = finding.get("type")
            remediation = RecommendationEngine.REMEDIATION_KB.get(finding_type)
            
            if remediation:
                recommendations.append({
                    "finding_id": finding.get("id"),
                    "finding_title": finding.get("title"),
                    "severity": finding.get("severity"),
                    "recommendation": remediation
                })
            else:
                # Default generic recommendation
                recommendations.append({
                    "finding_id": finding.get("id"),
                    "finding_title": finding.get("title"),
                    "severity": finding.get("severity"),
                    "recommendation": {
                        "title": f"Remediate {finding.get('title')}",
                        "description": "Apply security best practices to resolve this finding.",
                        "fix_steps": ["Review the finding details and apply necessary hardening steps."],
                        "reference": "N/A"
                    }
                })
        return recommendations
