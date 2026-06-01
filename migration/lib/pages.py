"""Disposition map for the 9 WP pages."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PageDisposition:
    action: str      # "import" | "skip"
    collection: str  # "posts" | "applied-musings" | ""
    draft: bool
    reason: str


_MAP: dict[str, PageDisposition] = {
    # Import as drafts in posts/ - need revising before publishing
    "johdatus-kayttaytymisarkkitehtuuriin": PageDisposition(
        action="import", collection="posts", draft=True,
        reason="published in WP; needs revising before re-publishing",
    ),
    "10-taitoa": PageDisposition(
        action="import", collection="posts", draft=True,
        reason="published in WP; needs revising before re-publishing",
    ),
    "yhteistyon-manifesti": PageDisposition(
        action="import", collection="posts", draft=True,
        reason="private in WP; never went live",
    ),
    # Skip
    "tervetuloa": PageDisposition(
        action="skip", collection="", draft=False,
        reason="home page already serves FI welcome",
    ),
    "reflektiota-oppimisesta-pohdintaa-lahtotilanteesta": PageDisposition(
        action="skip", collection="", draft=False,
        reason="uni-course reflection, not blog content",
    ),
    "sisallysluettelo": PageDisposition(
        action="skip", collection="", draft=False, reason="placeholder stub",
    ),
    "parempaa-ajattelua-rakentamassa": PageDisposition(
        action="skip", collection="", draft=False, reason="placeholder stub",
    ),
    "research-the-academic-stuff": PageDisposition(
        action="skip", collection="", draft=False,
        reason="2015 CV-style EN page; Google Scholar link covers it",
    ),
    "": PageDisposition(  # the empty-slug Welcome / Tervetuloa
        action="skip", collection="", draft=False,
        reason="lang-router stub; replaced by new home",
    ),
}


def disposition_for(slug: str) -> PageDisposition:
    """Return the import disposition for a WP page slug.

    Default is skip with a generic reason. Known slugs override.
    """
    return _MAP.get(
        slug,
        PageDisposition(
            action="skip", collection="", draft=False,
            reason="unknown page slug - review manually",
        ),
    )
