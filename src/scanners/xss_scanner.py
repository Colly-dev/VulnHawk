
"""
src/scanners/xss_scanner.py

Detects reflected and stored Cross-Site Scripting (XSS) vulnerabilities.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class XSSScanner:
    """
    Scans for Cross-Site Scripting (XSS) vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> List[str]:
        """
        Loads XSS payloads from the payloads/xss/payloads.txt file.
        """
        payload_file = "payloads/xss/payloads.txt"
        try:
            with open(payload_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"XSS payload file not found: {payload_file}")
            return ["<script>alert(1)</script>"] # Default payload

    async def scan(self, url: str, params: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Scans a given URL for XSS vulnerabilities.
        """
        findings = []
        logger.info(f"Scanning {url} for XSS...")

        # Example: Reflective XSS in URL parameters
        if params:
            for param, original_value in params.items():
                for payload in self.payloads:
                    test_params = params.copy()
                    test_params[param] = payload
                    response = await self.requester.get(url, params=test_params)
                    if response and payload in response.text:
                        findings.append({
                            "type": "Reflected XSS",
                            "severity": "High",
                            "cvss_score": 7.0, # Example CVSS score
                            "url": url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": f"Payload '{payload}' reflected in response.",
                            "remediation": "Sanitize user input before rendering in HTML."
                        })
                        logger.warning(f"XSS finding in {url} via parameter {param} with payload {payload}")

        # More sophisticated XSS detection logic would go here (e.g., stored XSS, DOM XSS)

        return findings
