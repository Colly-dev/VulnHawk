
import click
import sys
from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

# --- ETHICAL WARNING --- #
ETHICAL_WARNING = """
================================================================================
⚠️ CRITICAL ETHICAL WARNING ⚠️

SecureAudit is a security configuration auditing platform designed EXCLUSIVELY for:
- Auditing systems, websites, and cloud accounts you own or have explicit written authorization to assess
- Portfolio demonstration against your own test servers, local VMs, or free-tier cloud accounts
- Security consultants performing authorized client engagements

⚠️ DO NOT ⚠️
- ❌ Audit systems without explicit written authorization
- ❌ Use against production systems without proper change management
- ❌ Attempt to modify configurations or resources during audits
- ❌ Use for unauthorized penetration testing or security assessments

⚠️ REQUIREMENTS ⚠️
- ✅ Only audit systems you own or have explicit authorization to assess
- ✅ Use read-only checks whenever possible
- ✅ Store audit data securely and confidentially
- ✅ Comply with all applicable laws and regulations

⚠️ LIABILITY ⚠️
By using this software, you agree to:
- Use it responsibly and ethically
- Comply with all applicable laws
- Accept full responsibility for your actions
- Not use audit findings for malicious purposes

The authors assume NO LIABILITY for misuse, damage, or legal consequences
resulting from the use of this software.

USE RESPONSIBLY. STAY LEGAL. BE ETHICAL.
================================================================================
"""

ASCII_BANNER = """
  ___                            _   _             _     _ _   
 / __| ___  ___ __ _ _ _  _ _ __| |_(_)___ _ _  __| |___| | |_ 
 \__ \/ _ \/ -_) _` | ' \| '_/ _|  _| / _ \ ' \/ _` / -_) |  _|
 |___/\___/\___\__,_|_||_|_| \__|\__|_\___/_||_\__,_\___|_|\__|
                                                               
"""

@click.group()
def cli():
    """SecureAudit: Security Configuration Auditing Platform"""
    console.print(Text(ASCII_BANNER, style="bold green"))
    console.print(Panel(ETHICAL_WARNING, title="[bold red]ETHICAL USE WARNING[/bold red]", border_style="red"))
    console.print("\n[bold yellow]Welcome to SecureAudit! Use --help for available commands.[/bold yellow]")

@cli.command()
@click.option('--target', help='Target URL or host for web audit.')
def audit_web(target):
    """Audits web application security headers and TLS/SSL configuration."""
    console.print(f"[bold blue]Starting web audit for: {target}[/bold blue]")
    # Placeholder for web audit logic
    console.print("[green]Web audit completed (placeholder).[/green]")

@cli.command()
@click.option('--aws-profile', help='AWS profile to use for auditing.')
def audit_cloud_aws(aws_profile):
    """Audits AWS cloud configurations."""
    console.print(f"[bold blue]Starting AWS cloud audit using profile: {aws_profile}[/bold blue]")
    # Placeholder for AWS audit logic
    console.print("[green]AWS cloud audit completed (placeholder).[/green]")

@cli.command()
@click.option('--azure-subscription', help='Azure subscription ID for auditing.')
def audit_cloud_azure(azure_subscription):
    """Audits Azure cloud configurations."""
    console.print(f"[bold blue]Starting Azure cloud audit for subscription: {azure_subscription}[/bold blue]")
    # Placeholder for Azure audit logic
    console.print("[green]Azure cloud audit completed (placeholder).[/green]")

@cli.command()
@click.option('--host', help='Linux host to audit.')
@click.option('--ssh-user', help='SSH username for Linux host.')
@click.option('--ssh-key', help='Path to SSH private key for Linux host.')
def audit_linux(host, ssh_user, ssh_key):
    """Audits Linux OS hardening via SSH."""
    console.print(f"[bold blue]Starting Linux OS audit for {ssh_user}@{host}[/bold blue]")
    # Placeholder for Linux audit logic
    console.print("[green]Linux OS audit completed (placeholder).[/green]")

@cli.command()
def audit_windows():
    """Audits Windows OS hardening."""
    console.print("[bold blue]Starting Windows OS audit (local checks).[/bold blue]")
    # Placeholder for Windows audit logic
    console.print("[green]Windows OS audit completed (placeholder).[/green]")

@cli.command()
@click.option('--target', help='Target host or network for network audit.')
def audit_network(target):
    """Performs basic network security assessment."""
    console.print(f"[bold blue]Starting network audit for: {target}[/bold blue]")
    # Placeholder for network audit logic
    console.print("[green]Network audit completed (placeholder).[/green]")

@cli.command()
def audit_full():
    """Runs a full audit across all applicable modules."""
    console.print("[bold blue]Starting full audit...[/bold blue]")
    # Placeholder for full audit logic
    console.print("[green]Full audit completed (placeholder).[/green]")

@cli.command()
def runserver():
    """Starts the SecureAudit Flask web dashboard."""
    console.print("[bold blue]Starting Flask dashboard...[/bold blue]")
    # Placeholder for Flask app run logic
    console.print("[green]Flask dashboard started (placeholder).[/green]")

@cli.command()
@click.option('--audit-id', help='ID of the audit to generate reports for.')
@click.option('--format', type=click.Choice(['html', 'json', 'csv', 'pdf', 'all']), default='html', help='Report format.')
def report(audit_id, format):
    """Generates reports for a past audit."""
    console.print(f"[bold blue]Generating {format} report for audit ID: {audit_id}[/bold blue]")
    # Placeholder for report generation logic
    console.print("[green]Report generation completed (placeholder).[/green]")

@cli.command()
def seed():
    """Populates the database with demo data."""
    console.print("[bold blue]Seeding demo data...[/bold blue]")
    # Placeholder for data seeding logic
    console.print("[green]Demo data seeded (placeholder).[/green]")

if __name__ == '__main__':
    cli()
