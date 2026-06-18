# VulnHawk Architecture

```mermaid
graph LR
    A["vulnhawk.py<br/>(CLI Entry Point)"] --> B["src/core/scanner.py<br/>(Orchestrator)"]
    
    B --> C["Web Crawler<br/>(Link Discovery)"]
    B --> D["XSS Scanner<br/>(Reflected/Stored)"]
    B --> E["SQLi Scanner<br/>(Error/Boolean)"]
    B --> F["SSRF & LFI<br/>(Local/Remote)"]
    B --> G["XXE & SSTI<br/>(Injection)"]
    B --> H["Open Redirect<br/>(Phishing)"]
    B --> I["Header Security<br/>(CORS/HSTS)"]
    B --> J["Sensitive Data<br/>(Exposure)"]
    
    J --> K["Report Engine<br/>(HTML / JSON)"]
    
    style A fill:#2d5016,color:#fff,stroke:#1a3009,stroke-width:2px
    style B fill:#3d1a1a,color:#fff,stroke:#1a0a0a,stroke-width:2px
    style K fill:#2d5016,color:#fff,stroke:#1a3009,stroke-width:2px
    
    style C fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
    style D fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
    style E fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
    style F fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
    style G fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
    style H fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
    style I fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
    style J fill:#1a3a52,color:#fff,stroke:#0d1f2d,stroke-width:2px
```

## Architecture Overview

**VulnHawk** is a comprehensive security vulnerability scanner with the following components:

### Entry Point
- **vulnhawk.py** - Command-line interface entry point

### Core Orchestrator
- **src/core/scanner.py** - Central orchestrator that manages all scanning modules

### Security Scanners
1. **Web Crawler** - Discovers and crawls links
2. **XSS Scanner** - Detects reflected and stored XSS vulnerabilities
3. **SQLi Scanner** - Identifies SQL injection via error-based and boolean techniques
4. **SSRF & LFI** - Detects server-side request forgery and local file inclusion
5. **XXE & SSTI** - Scans for XML external entity and server-side template injection
6. **Open Redirect** - Identifies open redirect vulnerabilities
7. **Header Security** - Checks CORS and HSTS configurations
8. **Sensitive Data** - Detects exposed sensitive information

### Report Generation
- **Report Engine** - Outputs findings in HTML and JSON formats
