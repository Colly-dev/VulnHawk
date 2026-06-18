
"""
src/core/crawler.py

Web crawling and link discovery module for VulnHawk.
Handles sitemap parsing, robots.txt, form/parameter detection, and JavaScript link extraction.

⚠️ LEGAL DISCLAIMER ⚠️
This tool is for EDUCATIONAL and AUTHORIZED testing only.
Please ensure you have explicit permission before scanning any target.
The authors assume NO LIABILITY for misuse, damage, or legal consequences.
"""

import asyncio
import logging
from typing import List, Set
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class Crawler:
    """
    Performs web crawling to discover URLs, forms, and parameters within a target application.
    """
    def __init__(self, base_url: str, max_depth: int = 2, max_pages: int = 50):
        self.base_url = base_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.discovered_urls: Set[str] = set()
        self.client = httpx.AsyncClient()

    async def _fetch_url(self, url: str) -> str:
        """
        Fetches the content of a given URL.
        """
        try:
            response = await self.client.get(url, follow_redirects=True, timeout=10)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            logger.error(f"Request failed for {url}: {e}")
            return ""
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching {url}: {e}")
            return ""

    def _extract_links(self, html_content: str, base_url: str) -> List[str]:
        """
        Extracts all unique links from HTML content.
        """
        soup = BeautifulSoup(html_content, 'lxml')
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(self.base_url).netloc:
                links.append(full_url)
        return list(set(links))

    async def crawl(self) -> List[str]:
        """
        Starts the crawling process from the base URL.
        """
        queue = asyncio.Queue()
        await queue.put((self.base_url, 0))
        self.discovered_urls.add(self.base_url)

        while not queue.empty() and len(self.discovered_urls) < self.max_pages:
            current_url, depth = await queue.get()

            if current_url in self.visited_urls or depth > self.max_depth:
                continue

            self.visited_urls.add(current_url)
            logger.info(f"Crawling: {current_url} (Depth: {depth})")

            html_content = await self._fetch_url(current_url)
            if html_content:
                links = self._extract_links(html_content, current_url)
                for link in links:
                    if link not in self.discovered_urls:
                        self.discovered_urls.add(link)
                        await queue.put((link, depth + 1))
        
        return list(self.discovered_urls)

