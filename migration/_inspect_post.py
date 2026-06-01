"""One-off: inspect a single post's content:encoded from the WP XML."""
import sys
from lxml import etree

XML_PATH = r"C:\Users\qn353\Documents\git-projects\mattiheino-site\migration\source\andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml"

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
}

target = sys.argv[1] if len(sys.argv) > 1 else "10-taitoa"

tree = etree.parse(XML_PATH)
for item in tree.xpath("//item"):
    slug_el = item.xpath("wp:post_name", namespaces=NS)
    if not slug_el or slug_el[0].text != target:
        continue
    body = item.xpath("content:encoded", namespaces=NS)[0].text or ""
    print("=== slug:", target)
    print("=== body length:", len(body))
    print("=== <p tag count:", body.count("<p"))
    print("=== <br tag count:", body.count("<br"))
    print("=== \\n\\n count:", body.count("\n\n"))
    print("=== single \\n count:", body.count("\n"))
    print("=== first 2000 chars (repr) ===")
    print(repr(body[:2000]))
    break
