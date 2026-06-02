"""Map WordPress categories → frontmatter tag slugs."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from slugify import slugify


def _norm(s: str) -> str:
    """Lookup-normalise: NFKC, collapse whitespace (incl. NBSP), strip, lower.

    WP exports use NBSP (U+00A0) between glyphs like `º` and the first word,
    so a category like `º\\u00a0Data punk (English)` would never match a
    mapping written with a regular space without this pass.
    """
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def load_mapping(path: Path) -> dict[str, str]:
    """Parse a 'Category Name = tag-slug' file. Keys are lookup-normalised."""
    m: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = (s.strip() for s in line.split("=", 1))
        m[_norm(key)] = value
    return m


def categories_to_tags(categories: list[str], mapping: dict[str, str]) -> list[str]:
    """Translate a WP post's category list to a unique, ordered tag list.

    Mapping value `(skip)` drops the category entirely — useful for WP
    categories that aren't really topics (e.g. language-marker categories
    when language is already in frontmatter, or "Uncategorised").
    """
    if not categories:
        return ["uncategorised"]
    seen: set[str] = set()
    out: list[str] = []
    for c in categories:
        key = _norm(c)
        tag = mapping.get(key, slugify(key))
        if tag == "(skip)" or not tag:
            continue
        if tag not in seen:
            seen.add(tag)
            out.append(tag)
    return out or ["uncategorised"]
