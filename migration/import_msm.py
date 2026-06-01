"""Wayback recovery of motivationselfmanagement.com posts.

Reads:
  - migration/msm_inventory.py  (the 13-entry inventory)
  - migration/msm_cdx_cache.txt (latest CDX dump)

Writes (per recoverable post):
  - src/content/applied-musings/YYYY-MM-DD-<slug>.md (draft: true)
  - src/content/applied-musings/images/<slug>/*

Skips 'aloittaminen' with a note in migration/aloittaminen-decision.md.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from lxml import html as lhtml

from lib.html_to_md import sweep_shortcodes, to_markdown
from lib.images import (
    GDRIVE_FOLDER, MEDIA_ROOT, build_gdrive_index, build_media_index, rehost,
)
from lib.slug import normalise_slug
from lib.wayback import WaybackError, fetch_image_bytes, fetch_snapshot_html
from msm_inventory import INVENTORY, MSMPost


REPO_ROOT = Path(__file__).parent.parent
CDX_PATH = REPO_ROOT / "migration" / "msm_cdx_cache.txt"
CONTENT_ROOT = REPO_ROOT / "src" / "content" / "applied-musings"
ALOITTAMINEN_NOTE = REPO_ROOT / "migration" / "aloittaminen-decision.md"


def _best_snapshot(cdx_lines: list[str], slug: str) -> tuple[str, str] | None:
    """Find the latest 200 snapshot whose URL path ends in /<slug>/.

    Returns (canonical_url, timestamp) of the best match, or None. The site
    uses WordPress dated permalinks (/YYYY/MM/DD/<slug>/) so we slug-search
    rather than build URLs from inventory dates — handles permalink drift.
    """
    candidates = []
    needle = f"/{slug}/"
    for line in cdx_lines:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        original, timestamp, status = parts[0], parts[1], parts[2]
        if status != "200":
            continue
        path = urlparse(original).path
        if not path.endswith(needle):
            # Ignore /feed/, /trackback/ and other sub-resources.
            continue
        candidates.append((original, timestamp))
    if not candidates:
        return None
    candidates.sort(key=lambda ct: ct[1])  # by timestamp
    return candidates[-1]  # latest


def _extract_article(html: str) -> str:
    """Pull the <article> body from a Wayback snapshot."""
    tree = lhtml.fromstring(html)
    art = tree.xpath("//article")
    if not art:
        # Some themes wrap in <div class="entry-content">
        art = tree.xpath("//*[contains(@class, 'entry-content')]")
    if not art:
        raise RuntimeError("No <article> in snapshot")
    # Render the first match back to HTML
    return lhtml.tostring(art[0], encoding="unicode")


def _frontmatter(post: MSMPost) -> str:
    parts = [
        "---",
        f'title: "{post.title.replace(chr(34), chr(39))}"',
        f'description: "{post.title}"',
        f"published: {post.published.isoformat()}",
        f"lang: {post.lang}",
        "vetting_status: pending",
        "migration_source: motivationselfmanagement",
        "draft: true",
        f"msm_slug: \"{post.slug}\"",
        "tags: []",
        "---",
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cdx = CDX_PATH.read_text(encoding="utf-8").splitlines()
    media_index = build_media_index(REPO_ROOT / MEDIA_ROOT)
    gdrive_index = build_gdrive_index(GDRIVE_FOLDER)

    counts = {"ok": 0, "skipped": 0, "failed": 0, "images_ok": 0, "images_lost": 0}

    for post in INVENTORY:
        if post.slug == "aloittaminen":
            counts["skipped"] += 1
            if not args.dry_run:
                ALOITTAMINEN_NOTE.write_text(
                    "# `aloittaminen` decision pending\n\n"
                    "No individual Wayback snapshot. Options:\n"
                    "- Reconstruct from /blog/ index excerpt.\n"
                    "- Skip entirely (redirect to /applied-musings/).\n",
                    encoding="utf-8",
                )
            print(f"  skip  {post.slug}  (no individual Wayback snapshot)")
            continue

        match = _best_snapshot(cdx, post.slug)
        if match is None:
            counts["failed"] += 1
            print(f"  fail  {post.slug}  (no Wayback 200 snapshot)")
            continue
        url, ts = match

        # Throttle between posts so Wayback doesn't 429/503 us.
        time.sleep(2.0)
        try:
            html_doc = fetch_snapshot_html(url, ts)
            article_html = _extract_article(html_doc)
        except (WaybackError, RuntimeError) as e:
            counts["failed"] += 1
            print(f"  fail  {post.slug}  ({e})")
            continue

        new_slug = normalise_slug(post.slug)
        out_path = CONTENT_ROOT / f"{post.published.isoformat()}-{new_slug}.md"
        images_dir = CONTENT_ROOT / "images" / new_slug

        body_html = sweep_shortcodes(article_html)

        # Rehost images: WP-CDN refs via local tar; Wayback im_ for MSM uploads;
        # external dead → placeholder.
        IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
        for i, m in enumerate(IMG_RE.finditer(body_html), start=1):
            src = m.group(1)
            # Strip Wayback URL prefix if present in the snapshot's HTML.
            # Snapshot HTML rewrites both /web/<ts>/<url> and /web/<ts>im_/<url>
            # depending on whether the asset is a page or an image.
            src_clean = re.sub(
                r"^https?://web\.archive\.org/web/\d+(?:im_|cs_)?/", "", src
            )

            if "motivationselfmanagement.com/wp-content/uploads/" in src_clean:
                # Wayback im_ infix for MSM uploads. Throttle to avoid 429s.
                time.sleep(2.0)
                try:
                    data = fetch_image_bytes(src_clean, ts)
                    name = Path(urlparse(src_clean).path).name.lower()
                    images_dir.mkdir(parents=True, exist_ok=True)
                    outpath = images_dir / name
                    if not args.dry_run:
                        outpath.write_bytes(data)
                    body_html = body_html.replace(src, f"./images/{new_slug}/{name}", 1)
                    counts["images_ok"] += 1
                except WaybackError:
                    body_html = body_html.replace(m.group(0), f"<!-- IMAGE LOST: {src_clean} -->", 1)
                    counts["images_lost"] += 1
                continue

            # mattiheino.files.wordpress.com refs → local tar
            result = rehost(
                src_clean, slug=new_slug, dest=images_dir,
                media_index=media_index, gdrive_index=gdrive_index,
            )
            if result.status == "ok":
                body_html = body_html.replace(src, f"./images/{new_slug}/{result.local_path.name}", 1)
                counts["images_ok"] += 1
            else:
                body_html = body_html.replace(m.group(0), f"<!-- IMAGE LOST: {src_clean} -->", 1)
                counts["images_lost"] += 1

        body_md = to_markdown(body_html)
        full = _frontmatter(post) + body_md.strip() + "\n"

        if not args.dry_run:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(full, encoding="utf-8")
        counts["ok"] += 1
        print(f"  ok    {post.slug}")

    print("\n=== import_msm.py summary ===")
    for k, v in counts.items():
        print(f"  {k:14s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
