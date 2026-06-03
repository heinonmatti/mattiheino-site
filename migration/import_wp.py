"""WordPress eXtended RSS -> Astro content collection import.

One-shot pipeline. Reads:
  - migration/source/andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml
  - migration/source/media/ (untar'd)
  - migration/category-to-tag.txt
  - migration/post_collection_overrides.txt

Writes:
  - src/content/posts/YYYY-MM-DD-<slug>.md (+ images/<slug>/ folder)
  - src/content/applied-musings/YYYY-MM-DD-<slug>.md (+ images/<slug>/)
  - public/_redirects (append)
  - migration/dead-images-todo.md

Usage:
  cd migration && .venv/Scripts/activate
  python import_wp.py --dry-run    # no writes; report only
  python import_wp.py              # actual import
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from lib.categories import categories_to_tags, load_mapping
from lib.dead_images import DeadImageRow, write_worksheet
from lib.guid import feed_guid
from lib.html_to_md import sweep_shortcodes, to_markdown
from lib.images import (
    GDRIVE_FOLDER, MEDIA_ROOT, build_gdrive_index, build_media_index,
    classify_src, rehost,
)
from lib.lang import infer_lang
from lib.pages import disposition_for
from lib.slug import normalise_slug, redirect_lines_for, slug_from_title
from lib.wp_xml import WPItem, iter_items


REPO_ROOT = Path(__file__).parent.parent
XML_PATH = REPO_ROOT / "migration" / "source" / "andoutcomethesystemskyttytymisarkkitehtuuri.WordPress.2026-05-20.xml"
CONTENT_ROOT = REPO_ROOT / "src" / "content"
REDIRECTS_PATH = REPO_ROOT / "public" / "_redirects"
WORKSHEET_PATH = REPO_ROOT / "migration" / "dead-images-todo.md"
CATEGORY_MAP_PATH = REPO_ROOT / "migration" / "category-to-tag.txt"
OVERRIDES_PATH = REPO_ROOT / "migration" / "post_collection_overrides.txt"


_IMG_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)


def _load_overrides(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def _pick_collection(item: WPItem, overrides: set[str]) -> str:
    return "applied-musings" if item.slug in overrides else "posts"


def _frontmatter(item: WPItem, lang: str, tags: list[str], collection: str, draft: bool) -> str:
    description = (item.excerpt.strip()
                   or _first_paragraph(item.content_html)[:160].strip()
                   or item.title.strip())
    description = description.replace('"', "'")
    parts = [
        "---",
        f'title: "{item.title.replace(chr(34), chr(39))}"',
        f'description: "{description}"',
        f"published: {item.published.date().isoformat()}",
        f"lang: {lang}",
        "vetting_status: pending",
        "migration_source: mattiheino-wp",
        f"draft: {'true' if draft else 'false'}",
        f"tags: [{', '.join(repr(t) for t in tags)}]",
        f'wp_guid: "{feed_guid(item.guid)}"',
        "---",
        "",
    ]
    return "\n".join(parts)


def _first_paragraph(html: str) -> str:
    m = re.search(r"<p[^>]*>(.*?)</p>", html, re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    text = re.sub(r"<[^>]+>", "", m.group(1))
    return text


def _process_item(item: WPItem, collection: str, draft: bool,
                  media_index, gdrive_index, dead_rows: list[DeadImageRow],
                  category_map: dict[str, str], dry_run: bool,
                  counts: dict[str, int] | None = None) -> list[str]:
    """Return the list of _redirects lines emitted for this item."""
    new_slug = normalise_slug(item.slug)
    if not new_slug:
        # WP drafts often have no wp:post_name. Derive from title; if the title
        # also yields nothing, fall back to the publication date so paths stay
        # routable (no ./images// or /posts// double-slashes).
        date_fallback = f"untitled-{item.published.date().isoformat()}"
        new_slug = slug_from_title(item.title, fallback=date_fallback)
    out_path = CONTENT_ROOT / collection / f"{item.published.date().isoformat()}-{new_slug}.md"
    images_dir = CONTENT_ROOT / collection / "images" / new_slug

    lang = infer_lang(item.categories, item.content_html)
    tags = categories_to_tags(item.categories, category_map)
    body_html = sweep_shortcodes(item.content_html)

    # Rehost + rewrite images
    for i, m in enumerate(_IMG_RE.finditer(body_html), start=1):
        src = m.group(1)
        result = rehost(src, slug=new_slug, dest=images_dir,
                        media_index=media_index, gdrive_index=gdrive_index)
        if result.status == "ok":
            new_src = f"./images/{new_slug}/{result.local_path.name}"
            body_html = body_html.replace(src, new_src, 1)
            if counts is not None:
                counts["images_ok"] += 1
        else:
            placeholder = "<!-- IMAGE LOST: src=" + src + " -->"
            body_html = body_html.replace(m.group(0), placeholder, 1)
            dead_rows.append(DeadImageRow(
                collection=collection, slug=new_slug, paragraph=i,
                original=src, alt="",
            ))
            if counts is not None:
                counts["images_lost"] += 1

    body_md = to_markdown(body_html)
    fm = _frontmatter(item, lang, tags, collection, draft)
    full = fm + body_md.strip() + "\n"

    if not dry_run:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(full, encoding="utf-8")

    # Redirects (year + month + day from publish date). WP canonical
    # permalink on mattiheino.com is /YYYY/MM/DD/<slug>/.
    year = f"{item.published.year:04d}"
    month = f"{item.published.month:02d}"
    day = f"{item.published.day:02d}"
    new_path = f"/{collection}/{new_slug}/"
    return redirect_lines_for(
        wp_slug=item.slug, new_slug=new_slug, new_path=new_path,
        year=year, month=month, day=day,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    media_index = build_media_index(REPO_ROOT / MEDIA_ROOT)
    gdrive_index = build_gdrive_index(GDRIVE_FOLDER)
    overrides = _load_overrides(OVERRIDES_PATH)
    category_map = load_mapping(CATEGORY_MAP_PATH)

    dead_rows: list[DeadImageRow] = []
    redirect_lines: list[str] = []
    counts = {"published": 0, "drafts": 0, "pages_imported": 0,
              "pages_skipped": 0, "images_ok": 0, "images_lost": 0}

    for item in iter_items(XML_PATH):
        if item.post_type == "page":
            d = disposition_for(item.slug)
            if d.action == "skip":
                counts["pages_skipped"] += 1
                print(f"  skip page  {item.slug}  ({d.reason})")
                continue
            counts["pages_imported"] += 1
            redirect_lines.extend(_process_item(
                item, collection=d.collection, draft=d.draft,
                media_index=media_index, gdrive_index=gdrive_index,
                dead_rows=dead_rows, category_map=category_map,
                dry_run=args.dry_run, counts=counts,
            ))
            continue

        if item.post_type != "post":
            continue

        if item.status == "publish":
            counts["published"] += 1
            draft = False
        elif item.status == "draft":
            counts["drafts"] += 1
            draft = True
        else:
            continue  # private / pending / trash -> skip

        collection = _pick_collection(item, overrides)
        redirect_lines.extend(_process_item(
            item, collection=collection, draft=draft,
            media_index=media_index, gdrive_index=gdrive_index,
            dead_rows=dead_rows, category_map=category_map,
            dry_run=args.dry_run, counts=counts,
        ))

    if not args.dry_run:
        WORKSHEET_PATH.parent.mkdir(parents=True, exist_ok=True)
        write_worksheet(WORKSHEET_PATH, dead_rows)

        if redirect_lines:
            REDIRECTS_PATH.parent.mkdir(parents=True, exist_ok=True)
            existing = REDIRECTS_PATH.read_text(encoding="utf-8") if REDIRECTS_PATH.exists() else ""
            block = "# === BEGIN WP slug redirects (import_wp.py) ===\n"
            block += "\n".join(redirect_lines) + "\n"
            block += "# === END WP slug redirects ===\n"
            # Strip any prior version of this block before re-emitting
            cleaned = re.sub(
                r"# === BEGIN WP slug redirects[\s\S]*?# === END WP slug redirects ===\n?",
                "", existing,
            )
            REDIRECTS_PATH.write_text(cleaned + block, encoding="utf-8")

    print("\n=== import_wp.py summary ===")
    for k, v in counts.items():
        print(f"  {k:18s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
