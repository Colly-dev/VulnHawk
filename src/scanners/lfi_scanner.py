
"""
src/scanners/lfi_scanner.py

Detects Local File Inclusion (LFI) vulnerabilities.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class LFIScanner:
    """
    Scans for Local File Inclusion (LFI) vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> List[str]:
        """
        Loads LFI payloads from the payloads/lfi/payloads.txt file.
        """
        payload_file = "payloads/lfi/payloads.txt"
        try:
            with open(payload_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"LFI payload file not found: {payload_file}")
            return ["../../../../etc/passwd", "../etc/passwd"] # Default payloads

    async def scan(self, url: str, params: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Scans a given URL for LFI vulnerabilities.
        """
        findings = []
        logger.info(f"Scanning {url} for LFI...")

        if params:
            for param, original_value in params.items():
                for payload in self.payloads:
                    test_params = params.copy()
                    test_params[param] = payload
                    response = await self.requester.get(url, params=test_params)
                    if response and ("root:x:0:0" in response.text or "daemon:x:1:1" in response.text): # Example detection
                        findings.append({
                            "type": "Local File Inclusion",
                            "severity": "High",
                            "cvss_score": 7.8, # Example CVSS score
                            "url": url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": f"System file content detected with payload 
                                        '{payload}' in parameter '{param}'.",
                            "remediation": "Validate and sanitize user input, use a whitelist for file access, and avoid direct file path concatenation."
                        })
                        logger.warning(f"LFI finding in {url} via parameter {param} with payload {payload}")

        return findings
