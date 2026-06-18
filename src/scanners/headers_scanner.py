
"""
src/scanners/headers_scanner.py

Detects Missing or Misconfigured Security Headers.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class HeadersScanner:
    """
    Scans for missing or misconfigured security headers.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.security_headers = [
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Content-Security-Policy",
            "Permissions-Policy",
            "Referrer-Policy"
        ]

    async def scan(self, url: str) -> List[Dict[str, Any]]:
        """
        Scans a given URL for security header issues.
        """
        findings = []
        logger.info(f"Scanning {url} for Security Headers...")

        response = await self.requester.get(url)
        if not response:
            return findings

        headers = {k.lower(): v for k, v in response.headers.items()}

        # Check for missing headers
        for header in self.security_headers:
            if header.lower() not in headers:
                findings.append({
                    "type": "Missing Security Header",
                    "severity": "Medium",
                    "cvss_score": 4.0, # Example CVSS score
                    "url": url,
                    "evidence": f"Missing security header: {header}.",
                    "remediation": f"Implement the {header} header to enhance security."
                })
                logger.warning(f"Missing security header {header} in {url}")
        
        # Check for misconfigured CORS (wildcard)
        if "access-control-allow-origin" in headers and headers["access-control-allow-origin"] == "*":
            findings.append({
                "type": "Misconfigured CORS",
                "severity": "Medium",
                "cvss_score": 5.0, # Example CVSS score
                "url": url,
                "evidence": "Wildcard Access-Control-Allow-Origin header detected.",
                "remediation": "Restrict Access-Control-Allow-Origin to specific trusted domains."
            })
            logger.warning(f"Wildcard CORS detected in {url}")

        return findings
