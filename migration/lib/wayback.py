"""Wayback Machine fetch helpers."""
from __future__ import annotations

import time

import requests


class WaybackError(RuntimeError):
    pass


_HTML_TPL = "https://web.archive.org/web/{ts}/{url}"
_IMG_TPL = "https://web.archive.org/web/{ts}im_/{url}"
_UA = {"User-Agent": "mattiheino-site migration/0.0.1"}


def fetch_snapshot_html(url: str, timestamp: str, *, retries: int = 3, backoff: float = 1.5) -> str:
    """GET a Wayback HTML snapshot; retry on transient errors."""
    last = None
    for attempt in range(retries):
        r = requests.get(_HTML_TPL.format(ts=timestamp, url=url), headers=_UA, timeout=30)
        if r.status_code == 200:
            return r.text
        last = r
        time.sleep(backoff ** attempt)
    raise WaybackError(f"Wayback returned {last.status_code} for {url} @ {timestamp}")


def fetch_image_bytes(url: str, timestamp: str, *, retries: int = 3, backoff: float = 1.5) -> bytes:
    """GET an image via the Wayback 'im_' infix (returns the raw bytes, not a wrapped HTML page)."""
    last = None
    for attempt in range(retries):
        r = requests.get(_IMG_TPL.format(ts=timestamp, url=url), headers=_UA, timeout=30)
        if r.status_code == 200:
            return r.content
        last = r
        time.sleep(backoff ** attempt)
    raise WaybackError(f"Wayback returned {last.status_code} for image {url} @ {timestamp}")
