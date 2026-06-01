"""Wayback Machine fetch helpers."""
from __future__ import annotations

import time

import requests


class WaybackError(RuntimeError):
    pass


_HTML_TPL = "https://web.archive.org/web/{ts}/{url}"
_IMG_TPL = "https://web.archive.org/web/{ts}im_/{url}"
_UA = {"User-Agent": "mattiheino-site migration/0.0.1"}


def _retry_get(url: str, *, retries: int, backoff: float):
    """GET with exponential backoff over both HTTP errors AND connection errors.

    Wayback intermittently refuses TCP connections under heavy load; treat
    that as transient just like a 503.
    """
    last_status = None
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=_UA, timeout=30)
            if r.status_code == 200:
                return r
            last_status = r.status_code
        except requests.exceptions.RequestException as e:
            last_exc = e
        time.sleep(backoff ** attempt)
    if last_exc is not None:
        raise WaybackError(f"Wayback connection failed for {url}: {last_exc}")
    raise WaybackError(f"Wayback returned {last_status} for {url}")


def fetch_snapshot_html(url: str, timestamp: str, *, retries: int = 3, backoff: float = 1.5) -> str:
    """GET a Wayback HTML snapshot; retry on transient errors."""
    return _retry_get(
        _HTML_TPL.format(ts=timestamp, url=url),
        retries=retries, backoff=backoff,
    ).text


def fetch_image_bytes(url: str, timestamp: str, *, retries: int = 3, backoff: float = 1.5) -> bytes:
    """GET an image via the Wayback 'im_' infix (returns the raw bytes, not a wrapped HTML page)."""
    return _retry_get(
        _IMG_TPL.format(ts=timestamp, url=url),
        retries=retries, backoff=backoff,
    ).content
