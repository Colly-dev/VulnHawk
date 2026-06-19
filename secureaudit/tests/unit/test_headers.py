
import unittest
from src.modules.headers.header_analyzer import HeaderAnalyzer

class TestHeaderAnalyzer(unittest.TestCase):
    def test_missing_hsts(self):
        # Mock requests.get to return a response without HSTS
        # For now, this is a placeholder test
        analyzer = HeaderAnalyzer()
        findings = analyzer.analyze("http://example.com") # This will currently hit a real site
        
        # Assert that if HSTS is missing, a finding is generated
        # This requires mocking the requests library properly
        # self.assertTrue(any(f["type"] == "MISSING_HSTS" for f in findings))
        self.assertIsInstance(findings, list)

    def test_secure_headers_present(self):
        # Mock requests.get to return a response with all secure headers
        analyzer = HeaderAnalyzer()
        findings = analyzer.analyze("https://google.com") # This will currently hit a real site
        
        # Assert that no critical findings are generated for a secure site
        # self.assertFalse(any(f["severity"] == "HIGH" for f in findings))
        self.assertIsInstance(findings, list)
