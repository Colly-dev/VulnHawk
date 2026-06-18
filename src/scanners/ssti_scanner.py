
"""
src/scanners/ssti_scanner.py

Detects Server-Side Template Injection (SSTI) vulnerabilities.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class SSTIScanner:
    """
    Scans for Server-Side Template Injection (SSTI) vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> List[str]:
        """
        Loads SSTI payloads from the payloads/ssti/payloads.txt file.
        """
        payload_file = "payloads/ssti/payloads.txt"
        try:
            with open(payload_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"SSTI payload file not found: {payload_file}")
            return ["{{7*7}}", "${{7*7}}"] # Default payloads

    async def scan(self, url: str, params: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Scans a given URL for SSTI vulnerabilities.
        """
        findings = []
        logger.info(f"Scanning {url} for SSTI...")

        if params:
            for param, original_value in params.items():
                for payload in self.payloads:
                    test_params = params.copy()
                    test_params[param] = payload
                    response = await self.requester.get(url, params=test_params)
                    if response and "49" in response.text: # Example detection for {{7*7}}
                        findings.append({
                            "type": "Server-Side Template Injection",
                            "severity": "High",
                            "cvss_score": 7.3, # Example CVSS score
                            "url": url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": f"Template engine evaluated payload 
                                        '{payload}' in parameter '{param}'.",
                            "remediation": "Sanitize user input before rendering in templates, or use a secure template engine configuration."
                        })
                        logger.warning(f"SSTI finding in {url} via parameter {param} with payload {payload}")

        return findings
