
"""
src/core/requester.py

Centralized HTTP request handling for VulnHawk.
Manages timeouts, retries, rate-limiting, proxies, sessions, and custom headers.
"""

import httpx
import asyncio
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class Requester:
    """
    Handles all HTTP requests with robust features like retries, timeouts, and proxy support.
    """
    def __init__(self, 
                 timeout: int = 10, 
                 retries: int = 3, 
                 backoff_factor: float = 0.5, 
                 proxy: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None):
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.proxy = proxy
        self.headers = headers if headers else {
            "User-Agent": "VulnHawk/1.0 (Web Vulnerability Scanner; +https://github.com/Colly-Dev/VulnHawk)"
        }
        self.client = httpx.AsyncClient(timeout=self.timeout, proxies=self.proxy, headers=self.headers)

    async def send_request(self, 
                           method: str, 
                           url: str, 
                           **kwargs) -> Optional[httpx.Response]:
        """
        Sends an HTTP request with retry logic.
        """
        for attempt in range(self.retries):
            try:
                response = await self.client.request(method, url, **kwargs)
                response.raise_for_status() # Raise an exception for 4xx/5xx responses
                return response
            except httpx.RequestError as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.retries}) for {url}: {e}")
                if attempt < self.retries - 1:
                    await asyncio.sleep(self.backoff_factor * (2 ** attempt)) # Exponential backoff
                else:
                    logger.error(f"Max retries reached for {url}.")
            except Exception as e:
                logger.error(f"An unexpected error occurred while sending request to {url}: {e}")
                return None
        return None

    async def get(self, url: str, **kwargs) -> Optional[httpx.Response]:
        """
        Sends a GET request.
        """
        return await self.send_request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> Optional[httpx.Response]:
        """
        Sends a POST request.
        """
        return await self.send_request("POST", url, **kwargs)

    async def close(self):
        """
        Closes the HTTP client session.
        """
        await self.client.aclose()

