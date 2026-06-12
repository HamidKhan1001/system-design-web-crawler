import time
import pytest
from crawler import URLFrontier, URLItem


def test_push_new_url():
    f = URLFrontier()
    assert f.push(URLItem("https://a.com")) is True
    assert f.size == 1


def test_push_duplicate_rejected():
    f = URLFrontier()
    f.push(URLItem("https://a.com"))
    assert f.push(URLItem("https://a.com")) is False
    assert f.size == 1


def test_seen_count_increments():
    f = URLFrontier()
    f.push(URLItem("https://a.com"))
    f.push(URLItem("https://b.com"))
    assert f.seen_count == 2


def test_pop_any_returns_item():
    f = URLFrontier()
    f.push(URLItem("https://a.com", priority=5))
    item = f.pop_any()
    assert item is not None
    assert item.url == "https://a.com"


def test_pop_any_empty_returns_none():
    f = URLFrontier()
    assert f.pop_any() is None


def test_priority_order():
    f = URLFrontier(politeness_delay=0)
    f.push(URLItem("https://low.com", priority=1))
    f.push(URLItem("https://high.com", priority=10))
    first = f.pop_any()
    assert first.url == "https://high.com"


def test_politeness_blocks_same_domain():
    f = URLFrontier(politeness_delay=60.0)
    f.push(URLItem("https://example.com/p1"))
    f.push(URLItem("https://example.com/p2"))
    f.pop_any()  # fetch first — stamps domain time
    result = f.pop()  # second should be blocked
    assert result is None


def test_different_domains_not_blocked():
    f = URLFrontier(politeness_delay=0.0)
    f.push(URLItem("https://a.com"))
    f.push(URLItem("https://b.com"))
    assert f.pop_any() is not None
    assert f.pop_any() is not None
