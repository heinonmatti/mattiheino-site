"""Normalise WordPress post guids to match the LIVE RSS feed scheme.

Why this exists
---------------
WordPress.com's WXR export stores some post <guid> values as
``https://mattiheino.com/?p=N`` (posts created after the blog moved to HTTPS),
but the site's LIVE RSS feed serves *every* such guid over ``http://`` -- the
guid scheme is frozen at the blog's original http:// base and WordPress
normalises feed guids to it.

RSS readers dedupe on the exact <guid> string. Existing subscribers cached the
http:// form (that is what the feed has always served). If the new feed emits
https://, every affected post looks brand-new at the DNS cutover and the whole
archive is re-broadcast to subscribers. So the emitted guid MUST match the live
feed (http://), not the WXR export (https://).
"""
from __future__ import annotations

import re

# Only the numeric ?p= form is the frozen WP guid. Other domains (e.g. the
# motivationselfmanagement.com applied-musings guids) and permalink-style guids
# are left untouched.
_WP_P_GUID = re.compile(r"^https://(mattiheino\.com/\?p=\d+)$")


def feed_guid(guid: str) -> str:
    """Return the guid as the live WordPress RSS feed serves it.

    Downgrades the scheme of ``https://mattiheino.com/?p=N`` guids to ``http://``
    so existing subscribers' readers recognise the item and do not re-broadcast
    it. All other guids pass through unchanged.
    """
    return _WP_P_GUID.sub(r"http://\1", guid)
