
"""
src/utils/validators.py

Utility functions for URL and parameter validation, and input sanitization.
"""

import re
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class Validators:
    """
    Provides methods for validating URLs, parameters, and sanitizing input.
    """
    def __init__(self):
        pass

    def is_valid_url(self, url: str) -> bool:
        """
        Checks if the given string is a valid URL.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def sanitize_input(self, input_string: str) -> str:
        """
        Basic input sanitization to prevent common injection attacks.
        """
        # Remove common script tags and event handlers
        sanitized = re.sub(r'<script.*?>.*?</script>', '', input_string, flags=re.IGNORECASE)
        sanitized = re.sub(r'on[a-z]+=".*?"', '', sanitized, flags=re.IGNORECASE)
        # HTML entity encoding for <, >, &, ", 
        sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")
        sanitized = sanitized.replace("&", "&amp;").replace("\"", "&quot;")
        sanitized = sanitized.replace("\n", "").replace("\r", "")
        return sanitized

    def is_valid_ip_address(self, ip_string: str) -> bool:
        """
        Checks if the given string is a valid IPv4 or IPv6 address.
        """
        # Regex for IPv4
        ipv4_pattern = re.compile(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        # Regex for IPv6 (simplified)
        ipv6_pattern = re.compile(r"^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,7}:|^:([0-9a-fA-F]{1,4}:){1,6}$|^[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){1,6}:$")

        if ipv4_pattern.match(ip_string) or ipv6_pattern.match(ip_string):
            return True
        return False

