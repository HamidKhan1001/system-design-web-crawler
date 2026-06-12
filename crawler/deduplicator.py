import hashlib


class ContentDeduplicator:
    """
    Cryptographic SHA-256 deduplication of page content.
    Prevents re-indexing identical pages served at different URLs.
    """

    def __init__(self):
        self._seen: set = set()
        self._hash_to_url: dict = {}

    def is_duplicate(self, content: bytes) -> bool:
        h = self._fingerprint(content)
        return h in self._seen

    def register(self, url: str, content: bytes) -> bool:
        """Returns True if content is new, False if duplicate."""
        h = self._fingerprint(content)
        if h in self._seen:
            return False
        self._seen.add(h)
        self._hash_to_url[h] = url
        return True

    def fingerprint(self, content: bytes) -> str:
        return self._fingerprint(content)

    def _fingerprint(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @property
    def unique_count(self) -> int:
        return len(self._seen)
