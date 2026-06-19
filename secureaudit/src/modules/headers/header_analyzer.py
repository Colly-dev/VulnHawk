
import requests
from typing import List, Dict, Any

class HeaderAnalyzer:
    """
    Analyzes HTTP security headers for a given URL.
    """
    
    SECURITY_HEADERS = {
        "Strict-Transport-Security": {"severity": "HIGH", "type": "MISSING_HSTS"},
        "Content-Security-Policy": {"severity": "HIGH", "type": "MISSING_CSP"},
        "X-Frame-Options": {"severity": "MEDIUM", "type": "MISSING_XFO"},
        "X-Content-Type-Options": {"severity": "LOW", "type": "MISSING_XCTO"},
        "Referrer-Policy": {"severity": "LOW", "type": "MISSING_RP"},
        "Permissions-Policy": {"severity": "LOW", "type": "MISSING_PP"}
    }

    def analyze(self, url: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers

            for header, info in self.SECURITY_HEADERS.items():
                if header not in headers:
                    findings.append({
                        "id": f"WEB_HEADER_{header.replace('-', '_').upper()}",
                        "title": f"Missing Security Header: {header}",
                        "description": f"The security header '{header}' is not present in the HTTP response.",
                        "severity": info["severity"],
                        "type": info["type"],
                        "category": "Web Security"
                    })
                else:
                    # Optional: Add logic to check for weak values
                    pass
                    
        except Exception as e:
            findings.append({
                "id": "WEB_CONN_ERROR",
                "title": "Connection Error during Header Analysis",
                "description": str(e),
                "severity": "INFO",
                "type": "CONNECTION_ERROR",
                "category": "General"
            })
            
        return findings
