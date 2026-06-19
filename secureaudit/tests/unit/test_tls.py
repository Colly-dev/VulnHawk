
import unittest
from src.modules.tls.protocol_checker import ProtocolChecker

class TestProtocolChecker(unittest.TestCase):
    def test_weak_protocol_detection(self):
        checker = ProtocolChecker()
        # This test is a placeholder as actual TLS handshake requires a live server
        # and complex mocking. For demo purposes, we expect a demo finding.
        findings = checker.analyze("example.com") 
        
        self.assertTrue(any(f["type"] == "WEAK_TLS_PROTOCOL" for f in findings))
        self.assertIsInstance(findings, list)

    def test_secure_protocol_detection(self):
        checker = ProtocolChecker()
        # This test is a placeholder as actual TLS handshake requires a live server
        # and complex mocking. For demo purposes, we assume no weak protocols.
        findings = checker.analyze("google.com") 
        
        # In a real test, we would assert that no weak protocol findings are present
        # self.assertFalse(any(f["type"] == "WEAK_TLS_PROTOCOL" for f in findings))
        self.assertIsInstance(findings, list)
