from datetime import datetime
from lib.wp_xml import iter_items


def test_iter_items_yields_all_items(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    assert len(items) == 3


def test_iter_items_parses_first_post_fields(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    p = items[0]
    # Title is HTML-decoded (CDATA in WP exports preserves entity literals).
    assert p.title == "First post (Slides & deck)"
    assert p.slug == "first-post"
    assert p.status == "publish"
    assert p.post_type == "post"
    assert p.guid == "https://example.test/?p=1"
    assert p.published == datetime(2014, 11, 15, 10, 0, 0)
    # Categories include both domain="category" and domain="post_tag".
    assert "Complex systems" in p.categories
    assert "modeling" in p.categories
    assert "Bayesian analysis" in p.categories
    assert "Hello" in p.content_html


def test_iter_items_distinguishes_drafts(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    drafts = [i for i in items if i.status == "draft"]
    assert len(drafts) == 1
    assert drafts[0].slug == "draft-post"


def test_iter_items_picks_up_pages(fixtures_dir):
    items = list(iter_items(fixtures_dir / "sample_export.xml"))
    pages = [i for i in items if i.post_type == "page"]
    assert len(pages) == 1
    assert pages[0].slug == "tervetuloa"
