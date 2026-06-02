"""Parse a WordPress eXtended RSS (WXR) export."""
from __future__ import annotations

import html
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterator
from lxml import etree


NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}


@dataclass(frozen=True)
class WPItem:
    title: str
    slug: str
    status: str          # publish | draft | private | pending | ...
    post_type: str       # post | page | attachment | ...
    guid: str
    published: datetime
    categories: list[str]
    content_html: str
    excerpt: str


def _text(elem, xpath: str, ns: dict | None = None) -> str:
    nodes = elem.xpath(xpath, namespaces=ns or NS)
    if not nodes:
        return ""
    n = nodes[0]
    return (n.text or "") if hasattr(n, "text") else str(n)


def iter_items(xml_path: Path) -> Iterator[WPItem]:
    tree = etree.parse(str(xml_path))
    for item in tree.xpath("//item"):
        # WP wraps these in <![CDATA[...]]> so lxml hands back the literal
        # bytes — including HTML entities like &amp;. html.unescape() turns
        # those back into the characters they encode (& not &amp;).
        title = html.unescape(_text(item, "title"))
        slug = _text(item, "wp:post_name")
        status = _text(item, "wp:status")
        post_type = _text(item, "wp:post_type")
        guid = _text(item, "guid")
        pub_str = _text(item, "wp:post_date")
        try:
            published = datetime.strptime(pub_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            published = datetime(1970, 1, 1)
        # Merge WP categories (domain="category") AND tags (domain="post_tag")
        # into a single list. WP semantically distinguishes them; for our
        # purpose they're both "topical labels" and the schema unifies them.
        categories = [
            (c.text or "")
            for c in item.xpath(
                "category[@domain='category' or @domain='post_tag']"
            )
        ]
        content_html = _text(item, "content:encoded")
        excerpt = html.unescape(_text(item, "excerpt:encoded"))
        yield WPItem(
            title=title,
            slug=slug,
            status=status,
            post_type=post_type,
            guid=guid,
            published=published,
            categories=categories,
            content_html=content_html,
            excerpt=excerpt,
        )
