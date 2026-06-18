
"""
src/scanners/ssrf_scanner.py

Detects Server-Side Request Forgery (SSRF) vulnerabilities.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class SSRFScanner:
    """
    Scans for Server-Side Request Forgery (SSRF) vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> List[str]:
        """
        Loads SSRF payloads from the payloads/ssrf/payloads.txt file.
        """
        payload_file = "payloads/ssrf/payloads.txt"
        try:
            with open(payload_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"SSRF payload file not found: {payload_file}")
            return ["http://127.0.0.1", "http://localhost"] # Default payloads

    async def scan(self, url: str, params: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Scans a given URL for SSRF vulnerabilities.
        """
        findings = []
        logger.info(f"Scanning {url} for SSRF...")

        if params:
            for param, original_value in params.items():
                for payload in self.payloads:
                    test_params = params.copy()
                    test_params[param] = payload
                    response = await self.requester.get(url, params=test_params)
                    if response and ("root:x:0:0" in response.text or "Server: Apache" in response.text): # Example detection
                        findings.append({
                            "type": "Server-Side Request Forgery",
                            "severity": "High",
                            "cvss_score": 8.0, # Example CVSS score
                            "url": url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": f"Internal resource access or server banner detected with payload 
                                        '{payload}' in parameter '{param}'.",
                            "remediation": "Validate and sanitize all user-supplied URLs and restrict outbound requests."
                        })
                        logger.warning(f"SSRF finding in {url} via parameter {param} with payload {payload}")

        return findings
