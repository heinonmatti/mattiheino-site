import pytest
from lib.html_to_md import sweep_shortcodes, to_markdown


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
