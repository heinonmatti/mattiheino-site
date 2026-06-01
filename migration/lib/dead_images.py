"""Dead-image worksheet writer."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import groupby
from pathlib import Path


@dataclass(frozen=True)
class DeadImageRow:
    collection: str  # "posts" | "applied-musings"
    slug: str
    paragraph: int
    original: str
    alt: str


def write_worksheet(path: Path, rows: list[DeadImageRow]) -> None:
    """Emit a Markdown worksheet with one checkbox per row, grouped by collection."""
    lines = ["# Dead-image worksheet", "",
             "Each row: pick an image (from GDrive or anywhere), drop it into",
             "`src/content/<collection>/images/<slug>/`, replace the `[Image lost",
             "in migration]` placeholder in the post body with a proper `<Image>`",
             "reference, and tick the row.",
             ""]
    rows_sorted = sorted(rows, key=lambda r: (r.collection, r.slug, r.paragraph))
    for collection, group in groupby(rows_sorted, key=lambda r: r.collection):
        lines.append(f"## {collection}")
        lines.append("")
        for row in group:
            lines.append(f"- [ ] **{row.slug}** · ¶{row.paragraph}")
            lines.append(f"  - Original: `{row.original}`")
            lines.append(f"  - Alt: \"{row.alt}\"")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
