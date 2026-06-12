import heapq
import time
from collections import defaultdict
from .url import URLItem


class URLFrontier:
    """
    Priority queue URL frontier with per-domain politeness delays.
    Deduplicates via SHA-256 URL hash set.
    """

    def __init__(self, politeness_delay: float = 1.0):
        self._heap: list = []
        self._seen: set = set()
        self._domain_last_fetch: dict = defaultdict(float)
        self.politeness_delay = politeness_delay
        self._counter = 0  # tiebreaker

    def push(self, item: URLItem) -> bool:
        h = item.url_hash
        if h in self._seen:
            return False
        self._seen.add(h)
        heapq.heappush(self._heap, (-item.priority, self._counter, item))
        self._counter += 1
        return True

    def pop(self) -> URLItem | None:
        while self._heap:
            _, _, item = heapq.heappop(self._heap)
            now = time.monotonic()
            last = self._domain_last_fetch[item.domain]
            if now - last >= self.politeness_delay:
                self._domain_last_fetch[item.domain] = now
                return item
            # put back and signal not ready
            heapq.heappush(self._heap, (-item.priority, self._counter, item))
            self._counter += 1
            return None
        return None

    def pop_any(self) -> URLItem | None:
        """Pop ignoring politeness (for testing / forced drain)."""
        if not self._heap:
            return None
        _, _, item = heapq.heappop(self._heap)
        self._domain_last_fetch[item.domain] = time.monotonic()
        return item

    @property
    def size(self) -> int:
        return len(self._heap)

    @property
    def seen_count(self) -> int:
        return len(self._seen)
