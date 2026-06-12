from crawler import WebCrawler


def test_seed_adds_to_frontier():
    c = WebCrawler()
    c.seed(["https://a.com", "https://b.com"])
    assert c.frontier.size == 2


def test_process_new_page():
    c = WebCrawler()
    result = c.process_page("https://a.com", b"<html>hello</html>")
    assert result is True
    assert c.crawled_count == 1


def test_process_duplicate_skipped():
    c = WebCrawler()
    c.process_page("https://a.com", b"same content")
    result = c.process_page("https://b.com", b"same content")
    assert result is False
    assert c.duplicate_skips == 1


def test_process_enqueues_links():
    c = WebCrawler()
    c.process_page("https://a.com", b"page", links=["https://b.com", "https://c.com"])
    assert c.frontier.seen_count >= 2


def test_crawled_count_increments():
    c = WebCrawler()
    for i in range(5):
        c.process_page(f"https://site{i}.com", f"content{i}".encode())
    assert c.crawled_count == 5
