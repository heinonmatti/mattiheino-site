"""Slug normalisation + per-URL redirect emission."""
from __future__ import annotations


def normalise_slug(slug: str) -> str:
    """Lowercase + dash-separate, but preserve Finnish ä/ö/å."""
    out: list[str] = []
    for ch in slug.lower():
        if ch.isalnum() or ch in "äöå":
            out.append(ch)
        elif ch in " -_":
            if out and out[-1] != "-":
                out.append("-")
    return "".join(out).strip("-")


def redirect_lines_for(
    wp_slug: str,
    new_slug: str,
    new_path: str,
    year: str | None = None,
    month: str | None = None,
) -> list[str]:
    """Emit _redirects lines for a post.

    No-op when wp_slug == new_slug. Otherwise emit one or two 301s:
      - bare /<wp_slug>/ -> new_path
      - /<year>/<month>/<wp_slug>/ -> new_path (if year+month given)
    """
    if wp_slug == new_slug:
        return []
    lines = [f"/{wp_slug}/  {new_path}  301"]
    if year and month:
        lines.append(f"/{year}/{month}/{wp_slug}/  {new_path}  301")
    return lines
