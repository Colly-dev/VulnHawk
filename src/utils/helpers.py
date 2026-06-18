
"""
src/utils/helpers.py

General utility and helper functions for VulnHawk.
"""

import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def get_domain_from_url(url: str) -> str:
    """
    Extracts the domain name from a given URL.
    """
    try:
        parsed_uri = urlparse(url)
        return parsed_uri.netloc
    except Exception as e:
        logger.error(f"Error extracting domain from URL {url}: {e}")
        return ""

def is_same_domain(url1: str, url2: str) -> bool:
    """
    Checks if two URLs belong to the same domain.
    """
    return get_domain_from_url(url1) == get_domain_from_url(url2)

