"""One-off: inspect a single post's content:encoded from the WP XML."""
import sys
from lxml import etree

XML_PATH = r"C:\Users\qn353\Documents\git-projects\mattiheino-site\migration\source\andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml"
TARGET_SLUG = "tavallista-vai-taikaa"

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
}

tree = etree.parse(XML_PATH)
for item in tree.xpath("//item"):
    slug_el = item.xpath("wp:post_name", namespaces=NS)
    if not slug_el or slug_el[0].text != TARGET_SLUG:
        continue
    body = item.xpath("content:encoded", namespaces=NS)[0].text or ""
    print("=== body length:", len(body))
    print("=== <p tag count:", body.count("<p"))
    print("=== <br tag count:", body.count("<br"))
    print("=== double-newline count:", body.count("\n\n"))
    print("=== single-newline count:", body.count("\n"))
    print()
    print("=== first 1500 chars (repr to show whitespace) ===")
    print(repr(body[:1500]))
    break
