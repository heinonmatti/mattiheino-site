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


def test_redirect_lines_for_same_slug_and_same_path_returns_empty():
    # Pure no-op: WP URL would equal new URL (no prefix change). Currently
    # not exercised in production (new_path always carries /posts/ or
    # /applied-musings/ prefix), but cheap to guard.
    assert redirect_lines_for(wp_slug="foo", new_slug="foo", new_path="/foo/") == []


def test_redirect_lines_for_empty_wp_slug_returns_empty():
    # Regression: WP drafts and some published posts have empty <wp:post_name>.
    # Emitting `/  /posts/derived-slug/  301` (or worse, `//  /posts/.../  301`
    # after the leading slash collapse) creates an apex-hijacking 301.
    assert redirect_lines_for(wp_slug="", new_slug="derived", new_path="/posts/derived/") == []
    assert redirect_lines_for(
        wp_slug="", new_slug="derived", new_path="/posts/derived/",
        year="2015", month="01",
    ) == []


def test_redirect_lines_for_changed_slug_bare_variant():
    # The bare slug is emitted in BOTH the trailing-slash and the no-slash
    # form. Cloudflare Pages does not add a missing trailing slash before it
    # matches _redirects, so /<slug> (no slash) 404s unless it has its own
    # rule. WordPress resolved the bare slug directly; this preserves that.
    lines = redirect_lines_for(wp_slug="old-name", new_slug="new-name", new_path="/posts/new-name/")
    assert lines == [
        "/old-name/  /posts/new-name/  301",
        "/old-name  /posts/new-name/  301",
    ]


def test_redirect_lines_for_dated_wp_url_when_year_month_given():
    lines = redirect_lines_for(
        wp_slug="old-name", new_slug="new-name", new_path="/posts/new-name/",
        year="2014", month="11",
    )
    assert "/2014/11/old-name/  /posts/new-name/  301" in lines
    assert "/old-name/  /posts/new-name/  301" in lines
    assert "/old-name  /posts/new-name/  301" in lines  # no-slash bare twin
    # Dated forms keep the trailing slash only — no no-slash twin.
    assert "/2014/11/old-name  /posts/new-name/  301" not in lines


def test_redirect_lines_for_full_dated_url_when_day_given():
    # WP canonical permalink is /YYYY/MM/DD/<slug>/ — all inbound links use
    # this form, so the 3-segment dated rule is required, not optional.
    lines = redirect_lines_for(
        wp_slug="old-name", new_slug="new-name", new_path="/posts/new-name/",
        year="2014", month="11", day="03",
    )
    assert "/2014/11/03/old-name/  /posts/new-name/  301" in lines
    assert "/2014/11/old-name/  /posts/new-name/  301" in lines
    assert "/old-name/  /posts/new-name/  301" in lines
    assert "/old-name  /posts/new-name/  301" in lines  # no-slash bare twin
    # Only the bare slug gets a no-slash twin; dated forms do not.
    assert "/2014/11/old-name  /posts/new-name/  301" not in lines
    assert "/2014/11/03/old-name  /posts/new-name/  301" not in lines


def test_redirect_lines_for_same_slug_still_emits_prefix_change_rules():
    # Even when wp_slug == new_slug, the path prefix differs (/<slug>/ vs
    # /posts/<slug>/), so bare + dated redirects are required.
    lines = redirect_lines_for(
        wp_slug="thing", new_slug="thing", new_path="/posts/thing/",
        year="2015", month="04", day="18",
    )
    assert "/thing/  /posts/thing/  301" in lines
    assert "/thing  /posts/thing/  301" in lines  # no-slash bare twin
    assert "/2015/04/thing/  /posts/thing/  301" in lines
    assert "/2015/04/18/thing/  /posts/thing/  301" in lines


def test_redirect_lines_for_no_slash_twin_targets_canonical_slashed_path():
    # Regression for the /besp 404: the no-slash twin must point at the
    # canonical /posts/<slug>/ (WITH slash), so a bare inbound link reaches
    # the real page in a single hop.
    lines = redirect_lines_for(wp_slug="besp", new_slug="besp", new_path="/posts/besp/")
    assert "/besp/  /posts/besp/  301" in lines
    assert "/besp  /posts/besp/  301" in lines
