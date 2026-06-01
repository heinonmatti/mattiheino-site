import pytest
from lib.slug import normalise_slug, redirect_lines_for


def test_normalise_slug_lowercases():
    assert normalise_slug("Hello World") == "hello-world"


def test_normalise_slug_preserves_finnish_chars():
    # Astro content collection IDs allow Unicode; keep ä/ö/å
    assert normalise_slug("Käyttäytymisarkkitehtuuri") == "käyttäytymisarkkitehtuuri"


def test_redirect_lines_for_same_slug_returns_empty():
    assert redirect_lines_for(wp_slug="foo", new_slug="foo", new_path="/posts/foo/") == []


def test_redirect_lines_for_changed_slug_emits_two_variants():
    lines = redirect_lines_for(wp_slug="old-name", new_slug="new-name", new_path="/posts/new-name/")
    assert "/old-name/  /posts/new-name/  301" in lines
    assert any("/2014/" not in l for l in lines)


def test_redirect_lines_for_dated_wp_url_when_year_month_given():
    lines = redirect_lines_for(
        wp_slug="old-name", new_slug="new-name", new_path="/posts/new-name/",
        year="2014", month="11",
    )
    assert "/2014/11/old-name/  /posts/new-name/  301" in lines
    assert "/old-name/  /posts/new-name/  301" in lines
