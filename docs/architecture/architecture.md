# VulnHawk Architecture Overview

This document outlines the high-level architecture of the VulnHawk web vulnerability scanner.

## Core Components

- **CLI Entry Point (`vulnhawk.py`)**: Handles command-line arguments, displays banners and legal disclaimers, and orchestrates the scanning process.
- **Core Modules (`src/core/`)**: Contains the main logic for scanning, crawling, making requests, CVSS calculation, and report generation.
- **Scanner Modules (`src/scanners/`)**: Individual modules for detecting specific vulnerability types (e.g., XSS, SQLi, SSRF).
- **Exploit Modules (`src/exploits/`)**: Modules for generating Proof-of-Concept (PoC) examples and WAF detection.
- **Utility Modules (`src/utils/`)**: Helper functions for logging, validation, and general utilities.

## Workflow

1. **Initialization**: The `vulnhawk.py` script initializes the scanner and its components.
2. **Crawling**: The `crawler.py` module discovers URLs and parameters within the target application.
3. **Scanning**: Individual scanner modules are invoked against discovered targets, injecting payloads and analyzing responses.
4. **Reporting**: Findings are collected, scored using CVSS, and compiled into comprehensive HTML and JSON reports.

## Data Flow

```mermaid
graph TD
    A[User Input] --> B(vulnhawk.py)
    B --> C{Scanner Initialization}
    C --> D[Crawler (src/core/crawler.py)]
    D --> E[Discovered URLs/Parameters]
    E --> F[Scanner Orchestration (src/core/scanner.py)]
    F --> G{Individual Scanners (src/scanners/*)}
    G --> H[Requester (src/core/requester.py)]
    H --> I[Target Web Application]
    I --> H
    G --> J[Findings]
    J --> K[CVSS Calculation (src/core/cvss.py)]
    K --> L[Report Engine (src/core/report_engine.py)]
    L --> M[HTML/JSON Reports]
```

## Future Enhancements

- Integration with CI/CD pipelines.
- Advanced WAF bypass techniques.
- Machine learning for vulnerability detection.
