
import socket
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

class PortScanner:
    """
    Performs a basic, rate-limited TCP connect scan.
    """

    def __init__(self, timeout: float = 1.0, max_workers: int = 10):
        self.timeout = timeout
        self.max_workers = max_workers

    def scan_port(self, target: str, port: int) -> Dict[str, Any]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((target, port))
                if result == 0:
                    return {"port": port, "status": "open"}
        except:
            pass
        return {"port": port, "status": "closed"}

    def scan(self, target: str, ports: List[int]) -> List[Dict[str, Any]]:
        findings = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(lambda p: self.scan_port(target, p), ports))
        
        open_ports = [r for r in results if r["status"] == "open"]
        
        for r in open_ports:
            findings.append({
                "id": f"NET_PORT_OPEN_{r['port']}",
                "title": f"Open Port Detected: {r['port']}",
                "description": f"Port {r['port']} was found to be open on the target.",
                "severity": "LOW",
                "type": "OPEN_PORT",
                "category": "Network Security"
            })
            
        return findings
