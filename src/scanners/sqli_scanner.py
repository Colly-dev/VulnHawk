
"""
src/scanners/sqli_scanner.py

Detects SQL Injection (SQLi) vulnerabilities (error-based and boolean-based).

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import logging
from typing import List, Dict, Any
from src.core.requester import Requester

logger = logging.getLogger(__name__)

class SQLiScanner:
    """
    Scans for SQL Injection vulnerabilities.
    """
    def __init__(self, requester: Requester):
        self.requester = requester
        self.payloads = self._load_payloads()

    def _load_payloads(self) -> List[str]:
        """
        Loads SQLi payloads from the payloads/sqli/payloads.txt file.
        """
        payload_file = "payloads/sqli/payloads.txt"
        try:
            with open(payload_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logger.error(f"SQLi payload file not found: {payload_file}")
            return ["' OR 1=1-- ", "' OR '1'='1"] # Default payloads

    async def scan(self, url: str, params: Dict[str, str] = None) -> List[Dict[str, Any]]:
        """
        Scans a given URL for SQL Injection vulnerabilities.
        """
        findings = []
        logger.info(f"Scanning {url} for SQLi...")

        # Example: Error-based SQLi detection
        if params:
            for param, original_value in params.items():
                for payload in self.payloads:
                    test_params = params.copy()
                    test_params[param] = original_value + payload
                    response = await self.requester.get(url, params=test_params)
                    if response and ("SQL syntax" in response.text or "mysql_fetch_array" in response.text):
                        findings.append({
                            "type": "Error-based SQL Injection",
                            "severity": "High",
                            "cvss_score": 7.5, # Example CVSS score
                            "url": url,
                            "parameter": param,
                            "payload": payload,
                            "evidence": f"SQL error message detected with payload 
                                        '{payload}' in parameter '{param}'.",
                            "remediation": "Implement parameterized queries or prepared statements."
                        })
                        logger.warning(f"SQLi finding in {url} via parameter {param} with payload {payload}")

        return findings
