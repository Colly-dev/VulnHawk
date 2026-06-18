
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from src.scanners.xss_scanner import XSSScanner
from src.scanners.sqli_scanner import SQLiScanner
from src.scanners.ssrf_scanner import SSRFScanner
from src.scanners.lfi_scanner import LFIScanner
from src.scanners.xxe_scanner import XXEScanner
from src.scanners.ssti_scanner import SSTIScanner
from src.scanners.redirect_scanner import RedirectScanner
from src.scanners.exposure_scanner import ExposureScanner
from src.scanners.headers_scanner import HeadersScanner

@pytest.fixture
def mock_requester():
    requester = AsyncMock()
    requester.get.return_value = MagicMock(text="", status_code=200, headers={})
    requester.post.return_value = MagicMock(text="", status_code=200, headers={})
    return requester

@pytest.mark.asyncio
async def test_xss_scanner_no_xss(mock_requester):
    scanner = XSSScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert not findings

@pytest.mark.asyncio
async def test_xss_scanner_reflected_xss(mock_requester):
    mock_requester.get.return_value = MagicMock(text="<script>alert(1)</script>", status_code=200, headers={})
    scanner = XSSScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert len(findings) == 1
    assert findings[0]["type"] == "Reflected XSS"

@pytest.mark.asyncio
async def test_sqli_scanner_no_sqli(mock_requester):
    scanner = SQLiScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert not findings

@pytest.mark.asyncio
async def test_sqli_scanner_error_based_sqli(mock_requester):
    mock_requester.get.return_value = MagicMock(text="SQL syntax error", status_code=200, headers={})
    scanner = SQLiScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert len(findings) == 1
    assert findings[0]["type"] == "Error-based SQL Injection"

@pytest.mark.asyncio
async def test_ssrf_scanner_no_ssrf(mock_requester):
    scanner = SSRFScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert not findings

@pytest.mark.asyncio
async def test_ssrf_scanner_internal_ip_disclosure(mock_requester):
    mock_requester.get.return_value = MagicMock(text="root:x:0:0", status_code=200, headers={})
    scanner = SSRFScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert len(findings) == 1
    assert findings[0]["type"] == "Server-Side Request Forgery"

@pytest.mark.asyncio
async def test_lfi_scanner_no_lfi(mock_requester):
    scanner = LFIScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert not findings

@pytest.mark.asyncio
async def test_lfi_scanner_etc_passwd_disclosure(mock_requester):
    mock_requester.get.return_value = MagicMock(text="root:x:0:0", status_code=200, headers={})
    scanner = LFIScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert len(findings) == 1
    assert findings[0]["type"] == "Local File Inclusion"

@pytest.mark.asyncio
async def test_xxe_scanner_no_xxe(mock_requester):
    scanner = XXEScanner(mock_requester)
    findings = await scanner.scan("http://test.com", data="<data></data>")
    assert not findings

@pytest.mark.asyncio
async def test_xxe_scanner_etc_passwd_disclosure(mock_requester):
    mock_requester.post.return_value = MagicMock(text="root:x:0:0", status_code=200, headers={})
    scanner = XXEScanner(mock_requester)
    findings = await scanner.scan("http://test.com", data="<data></data>")
    assert len(findings) == 1
    assert findings[0]["type"] == "XML External Entity"

@pytest.mark.asyncio
async def test_ssti_scanner_no_ssti(mock_requester):
    scanner = SSTIScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert not findings

@pytest.mark.asyncio
async def test_ssti_scanner_math_evaluation(mock_requester):
    mock_requester.get.return_value = MagicMock(text="49", status_code=200, headers={})
    scanner = SSTIScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert len(findings) == 1
    assert findings[0]["type"] == "Server-Side Template Injection"

@pytest.mark.asyncio
async def test_redirect_scanner_no_redirect(mock_requester):
    mock_requester.get.return_value = MagicMock(status_code=200, headers={})
    scanner = RedirectScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={"param": "value"})
    assert not findings

@pytest.mark.asyncio
async def test_redirect_scanner_open_redirect(mock_requester):
    mock_requester.get.return_value = MagicMock(status_code=302, headers={
        "Location": "https://www.google.com"
    })
    scanner = RedirectScanner(mock_requester)
    findings = await scanner.scan("http://test.com", params={
        "param": "https://www.google.com"
    })
    assert len(findings) == 1
    assert findings[0]["type"] == "Open Redirect"

@pytest.mark.asyncio
async def test_exposure_scanner_no_exposure(mock_requester):
    mock_requester.get.return_value = MagicMock(status_code=404, headers={})
    scanner = ExposureScanner(mock_requester)
    findings = await scanner.scan("http://test.com")
    assert not findings

@pytest.mark.asyncio
async def test_exposure_scanner_env_file_exposure(mock_requester):
    mock_requester.get.return_value = MagicMock(status_code=200, text="DB_PASSWORD=secret", headers={})
    scanner = ExposureScanner(mock_requester)
    findings = await scanner.scan("http://test.com")
    assert len(findings) == 1
    assert findings[0]["type"] == "Sensitive Data Exposure"

@pytest.mark.asyncio
async def test_headers_scanner_no_missing_headers(mock_requester):
    mock_requester.get.return_value = MagicMock(status_code=200, headers={
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src \'self\'",
        "Permissions-Policy": "geolocation=()",
        "Referrer-Policy": "no-referrer"
    })
    scanner = HeadersScanner(mock_requester)
    findings = await scanner.scan("http://test.com")
    assert not findings

@pytest.mark.asyncio
async def test_headers_scanner_missing_header(mock_requester):
    mock_requester.get.return_value = MagicMock(status_code=200, headers={})
    scanner = HeadersScanner(mock_requester)
    findings = await scanner.scan("http://test.com")
    assert any(f["type"] == "Missing Security Header" for f in findings)

@pytest.mark.asyncio
async def test_headers_scanner_wildcard_cors(mock_requester):
    mock_requester.get.return_value = MagicMock(status_code=200, headers={
        "Access-Control-Allow-Origin": "*"
    })
    scanner = HeadersScanner(mock_requester)
    findings = await scanner.scan("http://test.com")
    assert any(f["type"] == "Misconfigured CORS" for f in findings)
