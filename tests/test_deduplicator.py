from crawler import ContentDeduplicator


def test_new_content_not_duplicate():
    d = ContentDeduplicator()
    assert d.is_duplicate(b"fresh content") is False


def test_registered_content_is_duplicate():
    d = ContentDeduplicator()
    d.register("https://a.com", b"same content")
    assert d.is_duplicate(b"same content") is True


def test_register_returns_true_for_new():
    d = ContentDeduplicator()
    assert d.register("https://a.com", b"hello") is True


def test_register_returns_false_for_duplicate():
    d = ContentDeduplicator()
    d.register("https://a.com", b"hello")
    assert d.register("https://b.com", b"hello") is False


def test_unique_count():
    d = ContentDeduplicator()
    d.register("https://a.com", b"aaa")
    d.register("https://b.com", b"bbb")
    d.register("https://c.com", b"aaa")  # dup
    assert d.unique_count == 2


def test_fingerprint_is_hex():
    d = ContentDeduplicator()
    fp = d.fingerprint(b"data")
    assert len(fp) == 64


def test_different_content_different_fingerprints():
    d = ContentDeduplicator()
    assert d.fingerprint(b"a") != d.fingerprint(b"b")
