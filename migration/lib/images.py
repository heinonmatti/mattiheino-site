"""Image rehost pipeline.

For each <img src> in an imported post body:
  - wp-cdn ref -> look up in untar'd media index; copy to post images dir
  - external ref -> try filename match against GDrive folder; on hit, copy
  - no match -> record as 'lost'; caller writes a placeholder + worksheet row
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


MEDIA_ROOT = Path("migration/source/media")
# Windows path; the POSIX /c/... form only works under MSYS2/Git Bash
GDRIVE_FOLDER = Path(r"C:\LocalData\hema\Google Drive\Wordpress")

# WP resize suffix pattern e.g. foo-300x200.jpg, bar-1024x768.png
_RESIZE_RE = re.compile(r"-\d+x\d+(?=\.[a-z]+$)", re.IGNORECASE)
_LEADING_HASH_RE = re.compile(r"^#")


@dataclass
class RehostResult:
    status: str         # "ok" | "lost"
    source: str | None  # "media" | "gdrive" | None
    local_path: Path | None  # destination on disk if ok


def classify_src(src: str) -> str:
    """Return 'wp-cdn' or 'external'."""
    u = urlparse(src)
    host = (u.netloc or "").lower()
    path = u.path
    if host.endswith("mattiheino.files.wordpress.com"):
        return "wp-cdn"
    if host == "mattiheino.com" and "/wp-content/uploads/" in path:
        return "wp-cdn"
    if host == "mattiheino.wordpress.com" and "/wp-content/uploads/" in path:
        return "wp-cdn"
    if not host and "/wp-content/uploads/" in path:
        return "wp-cdn"
    return "external"


def _normalise_basename(name: str) -> str:
    """For gdrive matching: lowercase, strip leading '#', strip WP resize suffix."""
    name = _LEADING_HASH_RE.sub("", name)
    name = _RESIZE_RE.sub("", name)
    return name.lower()


def build_media_index(root: Path) -> dict[str, Path]:
    """Walk the untar'd media tree. Map 'YYYY/MM/file.ext' -> Path."""
    idx: dict[str, Path] = {}
    for p in root.rglob("*"):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            idx[rel] = p
    return idx


def build_gdrive_index(root: Path) -> dict[str, Path]:
    """Index the GDrive folder by normalised basename.

    Walks recursively so images organised into per-year/per-post subdirectories
    (Matti's GDrive layout) are discovered. Returns an empty dict if the folder
    does not exist (GDrive not mounted).
    """
    idx: dict[str, Path] = {}
    if not root.exists():
        print(f"  [warn] GDrive folder not found, external images will be lost: {root}")
        return idx
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            idx[_normalise_basename(p.name)] = p
    return idx


def _extract_relpath_from_wp_cdn(src: str) -> str:
    """Strip the WP-CDN prefix to a 'YYYY/MM/file.ext' relpath."""
    u = urlparse(src)
    path = u.path
    marker = "/wp-content/uploads/"
    if marker in path:
        return path.split(marker, 1)[1]
    return path.lstrip("/")


def rehost(
    src: str,
    *,
    slug: str,
    dest: Path,
    media_index: dict[str, Path],
    gdrive_index: dict[str, Path],
) -> RehostResult:
    """Resolve src -> copy a file into dest/. Return RehostResult.

    dest is the post's images/<slug>/ directory; it's created if needed.
    """
    kind = classify_src(src)
    dest.mkdir(parents=True, exist_ok=True)

    if kind == "wp-cdn":
        rel = _extract_relpath_from_wp_cdn(src)
        if rel in media_index:
            srcpath = media_index[rel]
            # Lowercase the destination filename: Linux (CF Pages build) is
            # case-sensitive but Windows is not, so on Windows the disk can
            # silently end up with 'hspCorr.PNG' while the markdown reference
            # is 'hspcorr.png'. Local build passes; CF build fails.
            outpath = dest / srcpath.name.lower()
            shutil.copy2(srcpath, outpath)
            return RehostResult(status="ok", source="media", local_path=outpath)
        return RehostResult(status="lost", source=None, local_path=None)

    # external
    # URL-decode the path so basenames like 'm%C3%B6kkiheppu%20copy.jpg'
    # match the on-disk 'mökkiheppu copy.jpg' in the GDrive index.
    basename = unquote(Path(urlparse(src).path).name)
    key = _normalise_basename(basename)
    if key in gdrive_index:
        srcpath = gdrive_index[key]
        # Lowercase for cross-platform safety; see above.
        outpath = dest / srcpath.name.lower()
        shutil.copy2(srcpath, outpath)
        return RehostResult(status="ok", source="gdrive", local_path=outpath)
    return RehostResult(status="lost", source=None, local_path=None)
