
from typing import List, Dict, Any
from .engine import AuditEngine

class AuditManager:
    def __init__(self):
        self.engine = AuditEngine()

    def run_web_audit(self, target: str) -> Dict[str, Any]:
        # Import modules here to avoid circular imports
        from ..modules.headers.header_analyzer import HeaderAnalyzer
        from ..modules.tls.protocol_checker import ProtocolChecker
        
        self.engine.start_time = None # Reset
        # Implementation would call specific module methods
        # analyzer = HeaderAnalyzer()
        # results = analyzer.analyze(target)
        # self.engine.add_finding(...)
        
        return self.engine.start_audit(target, modules=['headers', 'tls'])

    def run_cloud_audit(self, provider: str, credentials: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation for AWS/Azure
        return self.engine.start_audit(provider, modules=['cloud'])

    def run_os_audit(self, os_type: str, target: str) -> Dict[str, Any]:
        # Implementation for Linux/Windows
        return self.engine.start_audit(target, modules=['os_hardening'])
