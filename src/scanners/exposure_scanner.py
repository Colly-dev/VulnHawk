
"""
src/scanners/exposure_scanner.py

Detects Sensitive Data / File Exposure vulnerabilities.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class ExposureScanner:
    """
    Scans for Sensitive Data / File Exposure vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.paths = self._load_paths()

    def _load_paths(self) -> List[str]:
        """
        Loads common exposed paths from a built-in list.
        """
        return [
            "/.env",
            "/.git/HEAD",
            "/config.php.bak",
            "/backup.zip",
            "/phpinfo.php"
        ]

    async def scan(self, url: str) -> List[Dict[str, Any]]:
        """
        Scans a given URL for Sensitive Data / File Exposure vulnerabilities.
        """
        findings = []
        logger.info(f"Scanning {url} for Sensitive Data Exposure...")

        for path in self.paths:
            test_url = url.rstrip('/') + path
            response = await self.requester.get(test_url)
            if response and response.status_code == 200:
                # Basic check, can be improved with content analysis
                findings.append({
                    "type": "Sensitive Data Exposure",
                    "severity": "High",
                    "cvss_score": 7.5, # Example CVSS score
                    "url": test_url,
                    "evidence": f"Sensitive file or path 
                                '{path}' is accessible.",
                    "remediation": "Restrict access to sensitive files and directories, or remove them from the web root."
                })
                logger.warning(f"Sensitive Data Exposure finding in {test_url}")

        return findings
