⚠️ LEGAL DISCLAIMER ⚠️
================================================================================
VulnHawk is a security testing tool designed for EDUCATIONAL PURPOSES and
AUTHORIZED SECURITY TESTING ONLY.

By using this software, you agree to:
- ONLY scan systems you own or have explicit written permission to test
- Comply with all applicable laws and regulations
- Accept full responsibility for your actions
- NOT use this tool for illegal or unauthorized activities

The authors assume NO LIABILITY for misuse, damage, or legal consequences
resulting from the use of this software.

USE RESPONSIBLY. STAY LEGAL. BE ETHICAL.
================================================================================

# VulnHawk - Elite Web Application Vulnerability Scanner

VulnHawk is a Python-powered web application vulnerability scanner demonstrating offensive security, AppSec, and automated vulnerability assessment capabilities. Suitable for a cybersecurity portfolio, GitHub showcase, and AppSec / penetration tester job applications.

## Features
- Web crawling and enumeration
- Scanning for common web vulnerabilities (XSS, SQLi, SSRF, LFI, XXE, SSTI, Open Redirects, Sensitive Data Exposure, Missing Security Headers)
- CVSS 3.1 scoring for findings
- Proof-of-Concept (PoC) exploit generation
- WAF detection/fingerprinting
- JSON and HTML report generation
- Concurrent scanning with `asyncio`
- Professional and portfolio-ready code quality

## Installation

```bash
git clone https://github.com/Colly-Dev/VulnHawk.git
cd VulnHawk
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 vulnhawk.py -u https://example.com --scan all --report html
```

## Legal Notice

This tool is intended for educational purposes and authorized security testing only. Misuse is strictly prohibited.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
