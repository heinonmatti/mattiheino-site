"""HTML -> Markdown conversion with WordPress shortcode + Gutenberg sweep."""
from __future__ import annotations

import re
from markdownify import markdownify as _md


_CAPTION_RE = re.compile(
    r"\[caption[^\]]*\](.*?)\[/caption\]",
    re.IGNORECASE | re.DOTALL,
)
_GUTENBERG_RE = re.compile(r"<!--\s*/?wp:[^>]*-->")
_MORE_RE = re.compile(r"<!--\s*more\s*-->", re.IGNORECASE)
_GALLERY_RE = re.compile(r"\[gallery[^\]]*\]", re.IGNORECASE)


def sweep_shortcodes(html: str) -> str:
    """Strip / replace WP shortcodes + Gutenberg block comments.

    - [caption ...]<img> caption[/caption]  -> inner content kept verbatim
    - <!-- wp:* --> / <!-- /wp:* -->        -> stripped
    - <!--more-->                            -> stripped
    - [gallery ids="..."]                    -> '<!-- TODO: gallery -->'
    """
    html = _CAPTION_RE.sub(lambda m: m.group(1), html)
    html = _GUTENBERG_RE.sub("", html)
    html = _MORE_RE.sub("", html)
    html = _GALLERY_RE.sub("<!-- TODO: gallery -->", html)
    return html


def to_markdown(html: str) -> str:
    """Convert sanitised HTML to Markdown via markdownify.

    Run sweep_shortcodes() first to clear WP-specific cruft, then convert.
    """
    return _md(html, heading_style="ATX", bullets="-")
