
import click
import sys
import os

# Add src/ to sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.core.scanner import Scanner
from src.utils.logger import setup_logging

# Legal Disclaimer Banner
LEGAL_DISCLAIMER = """
╔═══════════════════════════════════════════════════════════════╗
║  ⚠️  LEGAL NOTICE - READ CAREFULLY  ⚠️                      ║
║                                                              ║
║  VulnHawk is for EDUCATIONAL and AUTHORIZED testing only.   ║
║  Only scan systems you own or have permission to test.      ║
║                                                              ║
║  By using this tool you agree to:                           ║
║    • Only scan authorized targets                           ║
║    • Comply with all laws                                   ║
║    • Accept full responsibility                             ║
║                                                              ║
║  The authors assume NO LIABILITY for misuse.                ║
╚═══════════════════════════════════════════════════════════════╝
"""

ASCII_BANNER = """

██╗   ██╗██╗   ██╗██╗     ██╗  ██╗███╗   ██╗ ██████╗ ██╗    ██╗
██║   ██║██║   ██║██║     ██║  ██║████╗  ██║██╔═══██╗██║    ██║
██║   ██║██║   ██║██║     ███████║██╔██╗ ██║██║   ██║██║ █╗ ██║
██║   ██║██║   ██║██║     ██╔══██║██║╚██╗██║██║   ██║██║███╗██║
╚██████╔╝╚██████╔╝███████╗██║  ██║██║ ╚████║╚██████╔╝╚███╔███╔╝
 ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚══╝╚══╝ 
                                                               
           Elite Web Vulnerability Scanner v1.0.0
"""

@click.command()
@click.option('-u', '--url', required=True, help='Target URL to scan.')
@click.option('--scan', default='all', help='Comma-separated list of scanners to run (e.g., xss,sqli) or "all".')
@click.option('--report', default='html', help='Report format (html, json, or all).')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
def main(url, scan, report, verbose):
    """
    VulnHawk: Elite Web Application Vulnerability Scanner.

    This tool is for EDUCATIONAL and AUTHORIZED testing only.
    Please ensure you have explicit permission before scanning any target.
    """
    click.echo(ASCII_BANNER)
    click.echo(LEGAL_DISCLAIMER)

    if not click.confirm("Do you agree to these terms? (yes/no):"): 
        click.echo("\nExiting. You must agree to the terms to use VulnHawk.")
        sys.exit(1)

    setup_logging(verbose)
    click.echo(f"\nStarting scan on: {url}")
    click.echo(f"Scanners to run: {scan}")
    click.echo(f"Report format: {report}")

    # Initialize and run the scanner
    scanner = Scanner(target_url=url, enabled_scanners=scan.split(','), report_formats=report.split(','))
    scanner.run_scan()

    click.echo("\nScan complete.")

if __name__ == '__main__':
    main()
