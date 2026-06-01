"""Map WordPress categories → frontmatter tag slugs."""
from __future__ import annotations

from pathlib import Path
from slugify import slugify


def load_mapping(path: Path) -> dict[str, str]:
    """Parse a 'Category Name = tag-slug' file. Keys are lowercased."""
    m: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = (s.strip() for s in line.split("=", 1))
        m[key.lower()] = value
    return m


def categories_to_tags(categories: list[str], mapping: dict[str, str]) -> list[str]:
    """Translate a WP post's category list to a unique, ordered tag list."""
    if not categories:
        return ["uncategorised"]
    seen: set[str] = set()
    out: list[str] = []
    for c in categories:
        key = c.lower()
        tag = mapping.get(key, slugify(key))
        if tag and tag not in seen:
            seen.add(tag)
            out.append(tag)
    return out or ["uncategorised"]
