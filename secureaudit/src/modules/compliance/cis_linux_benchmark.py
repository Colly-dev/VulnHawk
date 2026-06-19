
import yaml
import os
from typing import List, Dict, Any

class CISLinuxBenchmark:
    """
    Validates systems against CIS Linux Benchmark controls.
    """

    def __init__(self, controls_path: str = "benchmarks/cis_linux/controls.yaml"):
        self.controls_path = controls_path
        self.controls = self._load_controls()

    def _load_controls(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.controls_path):
            return []
        with open(self.controls_path, 'r') as f:
            return yaml.safe_load(f) or []

    def evaluate(self, audit_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Maps audit findings to CIS controls and calculates compliance.
        """
        passed = 0
        failed = 0
        results = []

        # Simple mapping logic
        for control in self.controls:
            control_id = control.get("id")
            # Find if any finding matches this control
            is_failed = any(f.get("id") == control.get("mapping") for f in audit_results)
            
            status = "FAIL" if is_failed else "PASS"
            if status == "PASS": passed += 1
            else: failed += 1
            
            results.append({
                "id": control_id,
                "title": control.get("title"),
                "status": status,
                "severity": control.get("severity")
            })

        total = len(self.controls)
        score = (passed / total * 100) if total > 0 else 100

        return {
            "benchmark": "CIS Linux Benchmark",
            "score": round(score, 2),
            "passed": passed,
            "failed": failed,
            "total": total,
            "controls": results
        }
