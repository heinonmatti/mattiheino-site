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

# Block-level HTML elements. wpautop() does NOT wrap a chunk that already
# starts with one of these in a synthetic <p>. The list mirrors the
# defaults used by WordPress's wpautop() plus the elements we know turn up
# in Matti's WP export (figure, table, pre, blockquote, etc.).
_BLOCK_TAGS_RE = re.compile(
    r"^\s*</?(?:"
    r"h[1-6]|p|div|blockquote|ul|ol|li|dl|dt|dd|"
    r"pre|table|thead|tbody|tfoot|tr|th|td|"
    r"hr|figure|figcaption|"
    r"form|fieldset|"
    r"article|section|aside|nav|header|footer|main|"
    r"iframe|video|audio"
    r")[\s>/]",
    re.IGNORECASE,
)


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


_TRAILING_TEXT_RE = re.compile(
    # Closing top-level block tag immediately followed by a single newline
    # and then inline text. WP raw bodies frequently use a single \n here;
    # without escalation to \n\n the trailing paragraph glues onto the
    # previous list item / quote when markdownify processes the chunk.
    r"(</(?:ol|ul|blockquote|table|figure|pre|h[1-6]|div)>)\s*\n([^\n<\s])",
    re.IGNORECASE,
)

_LEADING_TEXT_RE = re.compile(
    # Mirror image: inline text directly followed by an opening top-level
    # block tag with only a single newline between them.
    r"([^\s<])\s*\n(<(?:ol|ul|blockquote|table|figure|pre|h[1-6]|div)[\s>])",
    re.IGNORECASE,
)


def wpautop(html: str) -> str:
    """Wrap blank-line-separated chunks in <p> tags (mirrors WP's wpautop).

    WordPress stores post bodies with `\\n\\n` between paragraphs and lets the
    rendering layer turn those into <p>...</p>. The WXR export preserves
    that raw form. Without wpautop, markdownify treats the whole body as
    inline text and collapses paragraph breaks.

    First normalise block-tag boundaries: when a closing top-level block tag
    is followed by single-newline + inline text (or vice versa), promote to
    `\\n\\n` so the splitter treats them as separate paragraphs. Otherwise
    a body like `<ol>...</ol>\\nTrailing paragraph` ends up wholly inside
    one chunk that starts with a block tag, so the trailing prose is left
    unwrapped and markdownify glues it onto the last list item.
    """
    html = _TRAILING_TEXT_RE.sub(r"\1\n\n\2", html)
    html = _LEADING_TEXT_RE.sub(r"\1\n\n\2", html)
    chunks = re.split(r"\n\n+", html.strip())
    out: list[str] = []
    for c in chunks:
        c = c.strip()
        if not c:
            continue
        if _BLOCK_TAGS_RE.match(c):
            out.append(c)
        else:
            out.append(f"<p>{c}</p>")
    return "\n\n".join(out)


def to_markdown(html: str) -> str:
    """Convert sanitised HTML to Markdown via markdownify.

    Run sweep_shortcodes() first to clear WP-specific cruft. Then apply
    wpautop() so paragraph breaks survive into the Markdown output.
    """
    return _md(wpautop(html), heading_style="ATX", bullets="-")
