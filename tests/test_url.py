from crawler import URLItem


def test_domain_extracted():
    item = URLItem(url="https://example.com/page")
    assert item.domain == "example.com"


def test_url_hash_is_hex():
    item = URLItem(url="https://example.com")
    assert len(item.url_hash) == 64


def test_same_url_same_hash():
    a = URLItem(url="https://x.com")
    b = URLItem(url="https://x.com")
    assert a.url_hash == b.url_hash


def test_different_urls_different_hashes():
    a = URLItem(url="https://a.com")
    b = URLItem(url="https://b.com")
    assert a.url_hash != b.url_hash


def test_priority_ordering():
    a = URLItem(url="https://a.com", priority=5)
    b = URLItem(url="https://b.com", priority=10)
    assert a < b
