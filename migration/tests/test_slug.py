import pytest
from lib.slug import normalise_slug, redirect_lines_for, slug_from_title


def test_normalise_slug_lowercases():
    assert normalise_slug("Hello World") == "hello-world"


def test_normalise_slug_empty_input_returns_empty():
    # Regression: blank WP <wp:post_name> produced './images//' paths
    # that broke the Astro/Vite image resolver on CF Pages.
    assert normalise_slug("") == ""


def test_slug_from_title_derives_from_title_when_title_present():
    assert slug_from_title("Covariates and Causality", fallback="x") == "covariates-and-causality"


def test_slug_from_title_returns_fallback_when_title_unslugifiable():
    assert slug_from_title("", fallback="untitled-2024-08-05") == "untitled-2024-08-05"
    assert slug_from_title("???   ", fallback="untitled-2024-08-05") == "untitled-2024-08-05"


def test_slug_from_title_caps_excessively_long_title():
    very_long = "a" * 200
    out = slug_from_title(very_long, fallback="x")
    assert len(out) <= 80
    assert out.startswith("a")


def test_normalise_slug_preserves_finnish_chars():
    # Astro content collection IDs allow Unicode; keep ä/ö/å
    assert normalise_slug("Käyttäytymisarkkitehtuuri") == "käyttäytymisarkkitehtuuri"


def test_redirect_lines_for_same_slug_returns_empty():
    assert redirect_lines_for(wp_slug="foo", new_slug="foo", new_path="/posts/foo/") == []


def test_redirect_lines_for_empty_wp_slug_returns_empty():
    # Regression: WP drafts and some published posts have empty <wp:post_name>.
    # Emitting `/  /posts/derived-slug/  301` (or worse, `//  /posts/.../  301`
    # after the leading slash collapse) creates an apex-hijacking 301.
    assert redirect_lines_for(wp_slug="", new_slug="derived", new_path="/posts/derived/") == []
    assert redirect_lines_for(
        wp_slug="", new_slug="derived", new_path="/posts/derived/",
        year="2015", month="01",
    ) == []


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
