
"""
src/core/report_engine.py

Generates JSON and HTML reports for VulnHawk findings.
Groups findings by severity, provides summaries, and remediation recommendations.
"""

import json
import logging
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
import os

logger = logging.getLogger(__name__)

class ReportEngine:
    """
    Handles the generation of various report formats based on scan findings.
    """
    def __init__(self):
        # Set up Jinja2 environment for HTML reports
        template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def _group_findings_by_severity(self, findings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Groups findings by their severity level.
        """
        grouped = {"Critical": [], "High": [], "Medium": [], "Low": [], "None": [], "Unknown": []}
        for finding in findings:
            severity = finding.get("severity", "Unknown")
            grouped[severity].append(finding)
        return grouped

    def generate_json_report(self, findings: List[Dict[str, Any]], output_path: str):
        """
        Generates a JSON report of the scan findings.
        """
        try:
            with open(output_path, 'w') as f:
                json.dump(findings, f, indent=4)
            logger.info(f"JSON report generated successfully: {output_path}")
        except IOError as e:
            logger.error(f"Error writing JSON report to {output_path}: {e}")

    def generate_html_report(self, findings: List[Dict[str, Any]], output_path: str):
        """
        Generates an HTML report of the scan findings.
        """
        try:
            template = self.jinja_env.get_template('report_template.html')
            grouped_findings = self._group_findings_by_severity(findings)
            
            # Basic statistics
            total_findings = len(findings)
            stats = {
                "total": total_findings,
                "critical": len(grouped_findings["Critical"]),
                "high": len(grouped_findings["High"]),
                "medium": len(grouped_findings["Medium"]),
                "low": len(grouped_findings["Low"]),
            }

            html_content = template.render(
                findings=grouped_findings,
                stats=stats,
                report_title="VulnHawk Scan Report",
                scan_date="June 18, 2026" # Placeholder
            )

            with open(output_path, 'w') as f:
                f.write(html_content)
            logger.info(f"HTML report generated successfully: {output_path}")
        except Exception as e:
            logger.error(f"Error generating HTML report to {output_path}: {e}")

