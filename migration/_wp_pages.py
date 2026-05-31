import xml.etree.ElementTree as ET
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, "source", "andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml")
OUT = os.path.join(_HERE, "_wp_pages.txt")
ns = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
}

tree = ET.parse(SRC)
channel = tree.getroot().find('channel')

def t(el, tag, nsk=None):
    return (el.findtext(tag, default='', namespaces=ns) if nsk else el.findtext(tag, default='')) or ''

pages = []
welcome_hits = []
for it in channel.findall('item'):
    ptype = t(it, 'wp:post_type', 1)
    title = t(it, 'title')
    content = t(it, 'content:encoded', 1)
    rec = {
        'type': ptype,
        'title': title.strip(),
        'slug': t(it, 'wp:post_name', 1),
        'status': t(it, 'wp:status', 1),
        'date': t(it, 'wp:post_date', 1)[:10],
        'content': content,
    }
    if ptype == 'page':
        pages.append(rec)
    low = title.lower()
    if 'welcome' in low or 'tervetuloa' in low or 'site index' in low or 'sisällys' in low:
        welcome_hits.append(rec)

# full dump of all pages to file
with open(OUT, 'w', encoding='utf-8') as f:
    for p in pages:
        f.write(f"### [{p['type']}] {p['title']} | slug={p['slug']} | {p['status']} | {p['date']} | {len(p['content'])} chars\n\n")
        f.write(p['content'])
        f.write("\n\n" + "=" * 90 + "\n\n")

print("--- ALL PAGES ---")
for p in pages:
    print(f"  [{p['status']:7}] {p['date']} | {len(p['content']):5} chars | slug={p['slug']!r} | {p['title']}")

print("\n--- WELCOME / TERVETULOA / SITE INDEX MATCHES (full content) ---")
for p in welcome_hits:
    print(f"\n=== [{p['type']}] {p['title']} ({p['status']}, {p['date']}, slug={p['slug']!r}, {len(p['content'])} chars) ===")
    print(p['content'][:6000])

print(f"\nFull page dump written to {OUT}")
