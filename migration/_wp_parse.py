import xml.etree.ElementTree as ET
from collections import Counter
from urllib.parse import urlparse
import csv, os, datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, "source", "andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml")
OUT_DIR = _HERE

ns = {
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
}

tree = ET.parse(SRC)
root = tree.getroot()
channel = root.find('channel')
items = channel.findall('item')

type_counter = Counter()
ps_counter = Counter()           # (type, status)
posts = []                       # post + page rows
attach_urls = []
cat_counter = Counter()
tag_counter = Counter()
dates = []

def t(el, tag, nsk=None):
    return (el.findtext(tag, default='', namespaces=ns) if nsk else el.findtext(tag, default='')) or ''

for it in items:
    ptype = t(it, 'wp:post_type', 1)
    status = t(it, 'wp:status', 1)
    title = t(it, 'title')
    name = t(it, 'wp:post_name', 1)
    date = t(it, 'wp:post_date', 1)
    link = t(it, 'link')
    type_counter[ptype] += 1

    if ptype in ('post', 'page'):
        ps_counter[(ptype, status)] += 1
        content = t(it, 'content:encoded', 1)
        posts.append({
            'type': ptype, 'status': status, 'date': date[:10],
            'slug': name, 'title': title.strip(),
            'chars': len(content), 'link': link,
        })
        if date[:10]:
            dates.append(date[:10])
        for cat in it.findall('category'):
            dom = cat.get('domain'); val = (cat.text or '').strip()
            if dom == 'category' and val:
                cat_counter[val] += 1
            elif dom == 'post_tag' and val:
                tag_counter[val] += 1
    elif ptype == 'attachment':
        au = t(it, 'wp:attachment_url', 1)
        if au:
            attach_urls.append(au)

# attachment host breakdown
host_counter = Counter(urlparse(u).netloc for u in attach_urls)

# write posts/pages CSV (sorted by date)
csv_path = os.path.join(OUT_DIR, '_wp_posts.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['type', 'status', 'date', 'slug', 'title', 'chars', 'link'])
    w.writeheader()
    for r in sorted(posts, key=lambda x: x['date']):
        w.writerow(r)

# write attachment URL list
att_path = os.path.join(OUT_DIR, '_wp_attachments.txt')
with open(att_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(attach_urls))

# compact summary
sum_path = os.path.join(OUT_DIR, '_wp_inventory.txt')
lines = []
lines.append('=== WP EXPORT INVENTORY: mattiheino.com ===')
lines.append(f'total <item> entries: {len(items)}')
lines.append('')
lines.append('-- counts by post_type --')
for k, v in type_counter.most_common():
    lines.append(f'  {k or "(none)"}: {v}')
lines.append('')
lines.append('-- posts/pages by (type, status) --')
for (pt, st), v in sorted(ps_counter.items()):
    lines.append(f'  {pt} / {st}: {v}')
lines.append('')
if dates:
    lines.append(f'-- post/page date range: {min(dates)} .. {max(dates)} --')
lines.append('')
lines.append(f'-- attachments: {len(attach_urls)} total --')
for host, v in host_counter.most_common():
    lines.append(f'  {host}: {v}')
lines.append('')
lines.append(f'-- categories used ({len(cat_counter)}) --')
for k, v in cat_counter.most_common(40):
    lines.append(f'  {k}: {v}')
lines.append('')
lines.append(f'-- tags used ({len(tag_counter)}) (top 30) --')
for k, v in tag_counter.most_common(30):
    lines.append(f'  {k}: {v}')
lines.append('')
lines.append('Files written:')
lines.append(f'  {csv_path}')
lines.append(f'  {att_path}')
lines.append(f'  {sum_path}')

with open(sum_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('\n'.join(lines))
