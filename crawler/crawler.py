import hashlib
from .url import URLItem
from .frontier import URLFrontier
from .deduplicator import ContentDeduplicator


class WebCrawler:
    def __init__(self, politeness_delay: float = 1.0, max_depth: int = 3):
        self.frontier = URLFrontier(politeness_delay)
        self.dedup = ContentDeduplicator()
        self.max_depth = max_depth
        self._crawled: list = []
        self._skipped_depth = 0
        self._skipped_dedup = 0

    def seed(self, urls: list) -> None:
        for url in urls:
            self.frontier.push(URLItem(url=url, depth=0, priority=10))

    def process_page(self, url: str, content: bytes, links: list = None) -> bool:
        """
        Simulate processing a fetched page.
        Returns True if content was new (not a duplicate).
        """
        if not self.dedup.register(url, content):
            self._skipped_dedup += 1
            return False
        self._crawled.append({"url": url, "size": len(content)})
        # Enqueue discovered links
        current_item = self.frontier._seen  # already tracked
        if links:
            depth = 1  # simplified — real impl tracks per-URL depth
            if depth <= self.max_depth:
                for link in links:
                    self.frontier.push(URLItem(url=link, depth=depth))
        return True

    @property
    def crawled_count(self) -> int:
        return len(self._crawled)

    @property
    def duplicate_skips(self) -> int:
        return self._skipped_dedup
