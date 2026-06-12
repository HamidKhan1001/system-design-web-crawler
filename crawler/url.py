import hashlib
from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass
class URLItem:
    url: str
    depth: int = 0
    priority: int = 0

    @property
    def domain(self) -> str:
        return urlparse(self.url).netloc

    @property
    def url_hash(self) -> str:
        return hashlib.sha256(self.url.encode()).hexdigest()

    def __lt__(self, other: "URLItem") -> bool:
        return self.priority < other.priority
