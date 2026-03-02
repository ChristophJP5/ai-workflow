#!/usr/bin/env python3
"""
URL Fetch - Fetch and extract content from URLs.
"""

import asyncio
from typing import Optional, Dict, Any


class URLFetch:
    """
    Tool for fetching content from URLs.
    """

    def __init__(self):
        """Initialize URL fetch tool."""
        pass

    async def fetch(self, url: str, max_chars: int = 10000) -> Optional[str]:
        """
        Fetch content from a URL.

        Args:
            url: URL to fetch
            max_chars: Maximum characters to return

        Returns:
            Extracted content or None
        """
        await self._log_operation(f"fetch: {url[:100]}")
        
        try:
            # Use web_fetch if available (from OpenClaw)
            # For now, simulate with basic HTTP
            import urllib.request
            import ssl
            
            # Create SSL context that doesn't verify (for demo)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
                content = response.read().decode('utf-8', errors='ignore')
                
                # Truncate if needed
                if len(content) > max_chars:
                    content = content[:max_chars] + "\n... [truncated]"
                
                return content
                
        except Exception as e:
            print(f"   Error fetching URL: {e}")
            return None

    async def fetch_markdown(self, url: str) -> Optional[str]:
        """
        Fetch and convert HTML to markdown.

        Args:
            url: URL to fetch

        Returns:
            Markdown content or None
        """
        await self._log_operation(f"fetch_markdown: {url[:100]}")
        
        try:
            # Try to use html2text if available
            content = await self.fetch(url)
            if content:
                try:
                    import html2text
                    converter = html2text.HTML2Text()
                    converter.ignore_links = False
                    markdown = converter.handle(content)
                    return markdown
                except ImportError:
                    # html2text not available, return plain text
                    return self._html_to_text(content)
        except Exception as e:
            print(f"   Error fetching markdown: {e}")
            
        return None

    def _html_to_text(self, html: str) -> str:
        """Simple HTML to text conversion."""
        import re
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    async def _log_operation(self, operation: str):
        """Log operation."""
        print(f"   🌐 URL: {operation}")
