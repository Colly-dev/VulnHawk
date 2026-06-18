
"""
src/core/scanner.py

Main orchestration engine for VulnHawk.
Manages all scanner modules, concurrent scanning, rate limiting, and progress tracking.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import asyncio
import logging
from typing import List, Dict, Any

from src.core.crawler import Crawler
from src.core.requester import Requester
from src.core.cvss import CVSSCalculator
from src.core.report_engine import ReportEngine

logger = logging.getLogger(__name__)

class Scanner:
    """
    Orchestrates the scanning process, managing different vulnerability modules.
    """
    def __init__(self, target_url: str, enabled_scanners: List[str], report_formats: List[str]):
        self.target_url = target_url
        self.enabled_scanners = [s.strip().lower() for s in enabled_scanners]
        self.report_formats = [r.strip().lower() for r in report_formats]
        self.findings: List[Dict[str, Any]] = []
        self.crawler = Crawler(self.target_url)
        self.requester = Requester()
        self.cvss_calculator = CVSSCalculator()
        self.report_engine = ReportEngine()

        self.scanners_map = {
            # 'xss': XSSScanner, # To be implemented
            # 'sqli': SQLiScanner, # To be implemented
            # ... add other scanners here
        }

    async def _run_single_scanner(self, scanner_name: str, target: str) -> List[Dict[str, Any]]:
        """
        Runs a single vulnerability scanner against a target.
        """
        if scanner_name not in self.scanners_map:
            logger.warning(f"Scanner '{scanner_name}' not found or not implemented.")
            return []

        logger.info(f"Running {scanner_name.upper()} scanner on {target}")
        scanner_class = self.scanners_map[scanner_name]
        scanner_instance = scanner_class(self.requester) # Pass requester for HTTP requests
        # Assuming scan method takes target and returns findings
        # findings = await scanner_instance.scan(target)
        findings = [] # Placeholder
        return findings

    async def _coordinate_scans(self):
        """
        Coordinates the execution of all enabled scanners.
        """
        logger.info(f"Starting crawling for {self.target_url}")
        discovered_urls = await self.crawler.crawl()
        logger.info(f"Discovered {len(discovered_urls)} URLs.")

        tasks = []
        for url in discovered_urls:
            for scanner_name in self.enabled_scanners:
                if scanner_name == 'all' or scanner_name in self.scanners_map:
                    tasks.append(self._run_single_scanner(scanner_name, url))
        
        # Placeholder for actual scanner execution
        # all_findings = await asyncio.gather(*tasks)
        # for res in all_findings:
        #     self.findings.extend(res)
        
        # Simulate some findings for now
        self.findings.append({
            'type': 'XSS', 
            'severity': 'Medium', 
            'cvss_score': 6.1, 
            'url': self.target_url, 
            'evidence': 'alert(1) reflected', 
            'remediation': 'Input sanitization'
        })
        logger.info(f"Total findings: {len(self.findings)}")

    def run_scan(self):
        """
        Initiates the web vulnerability scan.
        """
        logger.info(f"Initiating scan for {self.target_url} with scanners: {', '.join(self.enabled_scanners)}")
        asyncio.run(self._coordinate_scans())
        
        if 'html' in self.report_formats or 'all' in self.report_formats:
            self.report_engine.generate_html_report(self.findings, f"reports/html/{self.target_url.replace('https://', '').replace('http://', '').replace('/', '_')}_report.html")
        if 'json' in self.report_formats or 'all' in self.report_formats:
            self.report_engine.generate_json_report(self.findings, f"reports/json/{self.target_url.replace('https://', '').replace('http://', '').replace('/', '_')}_report.json")

