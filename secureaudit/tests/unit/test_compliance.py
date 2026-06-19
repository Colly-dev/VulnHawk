
import unittest
from src.modules.compliance.cis_linux_benchmark import CISLinuxBenchmark

class TestCISLinuxBenchmark(unittest.TestCase):
    def test_compliance_evaluation(self):
        benchmark = CISLinuxBenchmark(controls_path="./benchmarks/cis_linux/controls.yaml")
        
        # Simulate some audit results
        audit_results = [
            {"id": "LINUX_SSH_ROOT_LOGIN", "title": "SSH Root Login Enabled", "severity": "HIGH"},
            {"id": "WEB_HEADER_STRICT_TRANSPORT_SECURITY", "title": "Missing HSTS Header", "severity": "HIGH"}
        ]
        
        result = benchmark.evaluate(audit_results)
        
        self.assertIn("benchmark", result)
        self.assertIn("score", result)
        self.assertIn("passed", result)
        self.assertIn("failed", result)
        self.assertIn("total", result)
        self.assertIn("controls", result)
        
        # Check if the simulated findings correctly mark controls as failed
        failed_controls = [c for c in result["controls"] if c["status"] == "FAIL"]
        self.assertEqual(len(failed_controls), 2)
        self.assertTrue(any(c["id"] == "1.1.1" for c in failed_controls))
        self.assertTrue(any(c["id"] == "2.1.1" for c in failed_controls))

    def test_no_findings_full_compliance(self):
        benchmark = CISLinuxBenchmark(controls_path="./benchmarks/cis_linux/controls.yaml")
        audit_results = [] # No findings
        result = benchmark.evaluate(audit_results)
        
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["passed"], result["total"])
        self.assertEqual(result["failed"], 0)
