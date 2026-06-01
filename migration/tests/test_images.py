from pathlib import Path

import pytest

from lib.images import (
    GDRIVE_FOLDER, MEDIA_ROOT, classify_src, rehost,
    build_gdrive_index, build_media_index,
)


def test_classify_wp_cdn_with_uploads_prefix():
    assert classify_src("https://mattiheino.files.wordpress.com/wp-content/uploads/2014/11/foo.jpg") == "wp-cdn"


def test_classify_external():
    assert classify_src("https://daringtodo.com/wp-content/uploads/2010/07/x.jpg") == "external"


def test_classify_relative_assumed_wp_cdn():
    # WP exports sometimes have relative paths.
    assert classify_src("/wp-content/uploads/2014/11/foo.jpg") == "wp-cdn"


def test_build_media_index_maps_relative_paths(fixtures_dir, tmp_path):
    media = fixtures_dir / "media"
    idx = build_media_index(media)
    assert "2014/11/foo.jpg" in idx
    assert idx["2014/11/foo.jpg"].name == "foo.jpg"


def test_build_gdrive_index_strips_resize_suffix(fixtures_dir):
    idx = build_gdrive_index(fixtures_dir / "gdrive")
    assert "lottalosada.jpg" in idx


def test_rehost_wp_cdn_copies_from_media(fixtures_dir, tmp_path):
    media_idx = build_media_index(fixtures_dir / "media")
    gdrive_idx = build_gdrive_index(fixtures_dir / "gdrive")
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://mattiheino.files.wordpress.com/wp-content/uploads/2014/11/foo.jpg",
        slug="sample", dest=out, media_index=media_idx, gdrive_index=gdrive_idx,
    )
    assert result.status == "ok"
    assert result.local_path == out / "foo.jpg"
    assert (out / "foo.jpg").exists()


def test_rehost_external_matches_gdrive_by_basename(fixtures_dir, tmp_path):
    media_idx = build_media_index(fixtures_dir / "media")
    gdrive_idx = build_gdrive_index(fixtures_dir / "gdrive")
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://daringtodo.com/wp-content/uploads/2010/07/lottalosada-300x200.jpg",
        slug="sample", dest=out, media_index=media_idx, gdrive_index=gdrive_idx,
    )
    assert result.status == "ok"
    assert result.source == "gdrive"
    assert result.local_path == out / "lottalosada.jpg"


def test_rehost_missing_returns_placeholder(fixtures_dir, tmp_path):
    media_idx = build_media_index(fixtures_dir / "media")
    gdrive_idx = build_gdrive_index(fixtures_dir / "gdrive")
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://cdn.meme.am/instances/500x/57546405.jpg",
        slug="sample", dest=out, media_index=media_idx, gdrive_index=gdrive_idx,
    )
    assert result.status == "lost"
    assert result.local_path is None


def test_rehost_external_url_decodes_basename_with_hash(tmp_path):
    """Regression: Google Sites URLs encode '#' as '%23'; the on-disk
    file '#ideaFLAT.jpg' must still match."""
    gd = tmp_path / "gdrive"
    gd.mkdir()
    (gd / "#ideaFLAT.jpg").write_bytes(b"\x00")
    gdrive_idx = build_gdrive_index(gd)
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://017f78a8ef2e75364393781012bdcf164e72b925.googledrive.com/host/foo/%23ideaFLAT.jpg",
        slug="sample", dest=out, media_index={}, gdrive_index=gdrive_idx,
    )
    assert result.status == "ok"
    assert result.source == "gdrive"


def test_rehost_external_url_decodes_basename_with_utf8(tmp_path):
    """Regression: Google Sites URLs encode 'ö' as '%C3%B6' and ' ' as '%20'."""
    gd = tmp_path / "gdrive"
    gd.mkdir()
    (gd / "mökkiheppu copy.jpg").write_bytes(b"\x00")
    gdrive_idx = build_gdrive_index(gd)
    out = tmp_path / "posts/images/sample"
    result = rehost(
        "https://017f78a8ef2e75364393781012bdcf164e72b925.googledrive.com/host/foo/m%C3%B6kkiheppu%20copy.jpg",
        slug="sample", dest=out, media_index={}, gdrive_index=gdrive_idx,
    )
    assert result.status == "ok"
    assert result.source == "gdrive"
