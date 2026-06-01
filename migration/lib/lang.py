"""Language inference from WordPress category + body text."""
from __future__ import annotations

import re

_FI_CHARS = set("äöåÄÖÅ")
# Finnish-named WP categories from the export inventory.
# Conservative: if the category name contains any of these tokens, it's FI.
_FI_CATEGORY_TOKENS = {
    "käyttäytym", "varautu", "terveys", "hyvinvoint", "ilmahygien",
    "kompleks", "muutos", "psykolog", "ajattel", "kriisi",
    "yhteistyö", "suomeksi",
}
_EN_CATEGORY_TOKENS = {
    "complex systems", "behaviour", "uncertainty", "self-management",
    "decision-making", "preparedness", "health", "wellbeing", "well-being",
    "risk", "english",
}


def _category_votes(categories: list[str]) -> tuple[int, int]:
    fi = en = 0
    for c in categories:
        lc = c.lower()
        if any(tok in lc for tok in _FI_CATEGORY_TOKENS):
            fi += 1
        if any(tok in lc for tok in _EN_CATEGORY_TOKENS):
            en += 1
    return fi, en


def _body_heuristic(body: str) -> str:
    """Finnish-character ratio over a sample. If >0.5% of alphabetic chars
    are Finnish-specific, classify as fi. Empty body -> en (default)."""
    alpha = [c for c in body if c.isalpha()]
    if not alpha:
        return "en"
    fi_chars = sum(1 for c in alpha if c in _FI_CHARS)
    ratio = fi_chars / len(alpha)
    return "fi" if ratio > 0.005 else "en"


def infer_lang(categories: list[str], body: str) -> str:
    """Return 'fi' or 'en' for a post.

    Strategy:
      1. Category vote: count tokens matched in FI vs EN sets. Majority wins.
      2. On tie or zero votes: Unicode heuristic on body text.
    """
    fi, en = _category_votes(categories)
    if fi > en:
        return "fi"
    if en > fi:
        return "en"
    return _body_heuristic(body)
