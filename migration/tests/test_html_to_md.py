import pytest
from lib.html_to_md import sweep_shortcodes, to_markdown, wpautop


def test_strip_caption_shortcode_preserves_img_and_caption():
    src = (
        '[caption id="" align="alignnone" width="500"]'
        '<img class="x" src="http://e.com/i.jpg" alt="" width="500" />'
        ' My caption[/caption]'
    )
    out = sweep_shortcodes(src)
    assert "[caption" not in out
    assert "[/caption]" not in out
    assert "<img" in out
    assert "My caption" in out


def test_strip_gutenberg_block_comments():
    src = "<!-- wp:paragraph --><p>Hello</p><!-- /wp:paragraph -->"
    out = sweep_shortcodes(src)
    assert "wp:paragraph" not in out
    assert "<p>Hello</p>" in out


def test_strip_more_marker():
    src = "Intro<!--more-->Body"
    out = sweep_shortcodes(src)
    assert "more" not in out


def test_gallery_left_as_marker():
    src = '[gallery ids="1,2,3"]'
    out = sweep_shortcodes(src)
    assert "TODO: gallery" in out


def test_to_markdown_basic_paragraph():
    html = "<p>This is a <strong>test</strong>.</p>"
    md = to_markdown(html)
    assert md.strip() == "This is a **test**."


def test_to_markdown_preserves_links():
    html = '<p>See <a href="https://example.com">example</a>.</p>'
    md = to_markdown(html)
    assert "[example](https://example.com)" in md


def test_wpautop_wraps_blank_line_separated_paragraphs():
    # Raw form WP stores in WXR: blank lines, no <p> tags.
    html = "First para.\n\nSecond para.\n\nThird para."
    out = wpautop(html)
    assert out.count("<p>") == 3
    assert out.count("</p>") == 3


def test_wpautop_does_not_double_wrap_block_elements():
    html = (
        "First plain.\n\n"
        "<h1>Heading</h1>\n\n"
        "<blockquote>Quote.</blockquote>\n\n"
        "Last plain."
    )
    out = wpautop(html)
    # Two plain chunks => two synthetic <p>.
    assert out.count("<p>") == 2
    assert "<p><h1>" not in out
    assert "<p><blockquote>" not in out


def test_to_markdown_renders_paragraph_breaks_from_blank_lines():
    # Regression: imported bodies from WP XML lacked <p> tags, so
    # markdownify ran every paragraph together in the rendered post.
    html = "First.\n\nSecond.\n\nThird."
    md = to_markdown(html)
    # Markdown paragraph separator is a blank line.
    assert "\n\n" in md
    parts = [p.strip() for p in md.strip().split("\n\n") if p.strip()]
    assert parts == ["First.", "Second.", "Third."]
