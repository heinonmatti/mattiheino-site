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


def slug_from_title(title: str, fallback: str) -> str:
    """Derive a routable slug from a title.

    WP drafts often have empty <wp:post_name>; the title is the only signal
    we have. If the title also normalises to nothing, fall back (e.g. to the
    date) so we never emit empty-slug paths like /posts// or ./images//.
    """
    s = normalise_slug(title)
    if s:
        # Astro file routing breaks on very long slugs; cap to a generous bound.
        return s[:80].rstrip("-")
    return fallback


def redirect_lines_for(
    wp_slug: str,
    new_slug: str,
    new_path: str,
    year: str | None = None,
    month: str | None = None,
) -> list[str]:
    """Emit _redirects lines for a post.

    No-op when wp_slug == new_slug, or when wp_slug is empty (no canonical
    WP URL to redirect FROM — emitting `/  ...` or `//  ...` would hijack
    the apex after Cloudflare path normalisation).

    Otherwise emit one or two 301s:
      - bare /<wp_slug>/ -> new_path
      - /<year>/<month>/<wp_slug>/ -> new_path (if year+month given)
    """
    if not wp_slug:
        return []
    if wp_slug == new_slug:
        return []
    lines = [f"/{wp_slug}/  {new_path}  301"]
    if year and month:
        lines.append(f"/{year}/{month}/{wp_slug}/  {new_path}  301")
    return lines
