# system-design-web-crawler

Scalable web crawler with a stateful URL frontier, per-domain politeness delays, and cryptographic content deduplication.

## Architecture

```
seed(urls)
    │
    ▼
URLFrontier (priority heap + SHA-256 seen set)
    │
  pop()  ←── politeness: wait ≥ 1s between requests to same domain
    │
 fetch page
    │
ContentDeduplicator.register(url, content)
    ├── SHA-256(content) already seen? → skip
    └── new → index + enqueue discovered links back to frontier
```

## Deep-dive metrics

| Concern | Solution |
|---------|---------|
| URL dedup | SHA-256 hash set — O(1) lookup, 32-byte fingerprint |
| Content dedup | SHA-256(page_bytes) — catches mirrors/duplicates at different URLs |
| Politeness | Per-domain last-fetch timestamp; blocks re-fetch within delay window |
| Priority | Max-heap — high-priority seeds (PageRank-like score) fetched first |

## Politeness delay

Each domain tracks `last_fetch_time`. `pop()` returns `None` if the domain was fetched within `politeness_delay` seconds, preventing IP bans and respecting `robots.txt` spirit.

## Running tests

```bash
pip install -r requirements.txt
python3 -m pytest tests/ -v   # 25 tests
```
