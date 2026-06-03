from lib.guid import feed_guid


def test_downgrades_https_p_guid():
    # The bug: WXR stored https for 2021-2025 posts; the live feed serves http.
    assert feed_guid("https://mattiheino.com/?p=4837") == "http://mattiheino.com/?p=4837"


def test_leaves_http_p_guid_unchanged():
    assert feed_guid("http://mattiheino.com/?p=123") == "http://mattiheino.com/?p=123"


def test_leaves_other_domains_unchanged():
    # motivationselfmanagement.com (applied-musings) guids must not be touched.
    g = "https://motivationselfmanagement.com/?p=9"
    assert feed_guid(g) == g


def test_leaves_permalink_style_guid_unchanged():
    # Only the numeric ?p= form is the frozen WP guid; don't rewrite permalinks.
    g = "https://mattiheino.com/2023/05/30/some-slug/"
    assert feed_guid(g) == g
