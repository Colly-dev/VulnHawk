
import json
import csv
import os
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any, List

class ReportEngine:
    """
    Generates audit reports in multiple formats.
    """

    def __init__(self, templates_dir: str = "src/dashboard/templates/reports"):
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def generate_json(self, audit_data: Dict[str, Any], output_path: str):
        with open(output_path, 'w') as f:
            json.dump(audit_data, f, indent=4)
        return output_path

    def generate_csv(self, findings: List[Dict[str, Any]], output_path: str):
        if not findings:
            return None
            
        keys = findings[0].keys()
        with open(output_path, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(findings)
        return output_path

    def generate_html(self, audit_data: Dict[str, Any], template_name: str, output_path: str):
        template = self.env.get_template(template_name)
        html_content = template.render(audit=audit_data)
        with open(output_path, 'w') as f:
            f.write(html_content)
        return output_path

    def generate_pdf(self, html_path: str, output_path: str):
        # This would use weasyprint or similar
        # For now, it's a placeholder
        from ..utils.pdf_generator import PDFGenerator
        pdf_gen = PDFGenerator()
        return pdf_gen.generate(html_path, output_path)
