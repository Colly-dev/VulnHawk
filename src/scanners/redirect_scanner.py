
"""
src/scanners/redirect_scanner.py

Detects Open Redirect vulnerabilities.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class RedirectScanner:
    """
    Scans for Open Redirect vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> List[str]:
        """
        Loads Open Redirect payloads from the payloads/redirect/payloads.txt file.
        """
        payload_file = "payloads/redirect/payloads.txt"
        try:
            with open(payload_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"Open Redirect payload file not found: {payload_file}")
            return ["https://www.google.com", "//google.com"] # Default payloads

    async def scan(self, url: str, params: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Scans a given URL for Open Redirect vulnerabilities.
        """
        findings = []
        logger.info(f"Scanning {url} for Open Redirect...")

        if params:
            for param, original_value in params.items():
                for payload in self.payloads:
                    test_params = params.copy()
                    test_params[param] = payload
                    response = await self.requester.get(url, params=test_params, follow_redirects=False)
                    if response and response.status_code in [301, 302, 303, 307, 308]:
                        location = response.headers.get('Location')
                        if location and payload in location:
                            findings.append({
                                "type": "Open Redirect",
                                "severity": "Medium",
                                "cvss_score": 6.1, # Example CVSS score
                                "url": url,
                                "parameter": param,
                                "payload": payload,
                                "evidence": f"Redirect to 
                                            '{location}' detected with payload 
                                            '{payload}' in parameter '{param}'.",
                                "remediation": "Validate and whitelist redirect URLs, or use a neutral interstitial page."
                            })
                            logger.warning(f"Open Redirect finding in {url} via parameter {param} with payload {payload}")

        return findings
