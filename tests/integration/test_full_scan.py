
import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from src.core.scanner import Scanner
import os

@pytest.mark.asyncio
async def test_full_scan_workflow():
    # Mock external dependencies like network requests and file writing
    with patch("src.core.crawler.Crawler.crawl", new_callable=AsyncMock) as mock_crawl,
         patch("src.core.requester.Requester.send_request", new_callable=AsyncMock) as mock_send_request,
         patch("src.core.report_engine.ReportEngine.generate_html_report") as mock_html_report,
         patch("src.core.report_engine.ReportEngine.generate_json_report") as mock_json_report:

        # Simulate discovered URLs from crawler
        mock_crawl.return_value = ["http://test.com/page1", "http://test.com/page2"]

        # Simulate responses for the requester
        mock_response_200 = AsyncMock()
        mock_response_200.status_code = 200
        mock_response_200.text = "<html><body>Hello</body></html>"
        mock_response_200.headers = {}
        mock_send_request.return_value = mock_response_200

        # Initialize scanner with a mock target and all scanners enabled
        scanner = Scanner(
            target_url="http://test.com",
            enabled_scanners=["xss", "sqli", "ssrf", "lfi", "xxe", "ssti", "redirect", "exposure", "headers"],
            report_formats=["html", "json"]
        )

        # Temporarily add mock scanners to the scanner_map for testing
        class MockXSSScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url, params=None): return []
        class MockSQLiScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url, params=None): return []
        class MockSSRFScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url, params=None): return []
        class MockLFIScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url, params=None): return []
        class MockXXEScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url, data=None): return []
        class MockSSTIScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url, params=None): return []
        class MockRedirectScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url, params=None): return []
        class MockExposureScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url): return []
        class MockHeadersScanner:
            def __init__(self, requester): self.requester = requester
            async def scan(self, url): return []

        scanner.scanners_map = {
            "xss": MockXSSScanner,
            "sqli": MockSQLiScanner,
            "ssrf": MockSSRFScanner,
            "lfi": MockLFIScanner,
            "xxe": MockXXEScanner,
            "ssti": MockSSTIScanner,
            "redirect": MockRedirectScanner,
            "exposure": MockExposureScanner,
            "headers": MockHeadersScanner,
        }

        # Run the scan
        scanner.run_scan()

        # Assertions
        mock_crawl.assert_called_once_with()
        # The number of calls to send_request will depend on the number of discovered URLs and scanners
        # For this basic test, we just check if it was called at all
        assert mock_send_request.called
        mock_html_report.assert_called_once()
        mock_json_report.assert_called_once()

        # Clean up generated report files if any (though mocks prevent actual file creation)
        # This part is more for real integration tests that don\'t mock file I/O
        html_report_path = f"reports/html/test_com_report.html"
        json_report_path = f"reports/json/test_com_report.json"
        if os.path.exists(html_report_path): os.remove(html_report_path)
        if os.path.exists(json_report_path): os.remove(json_report_path)
