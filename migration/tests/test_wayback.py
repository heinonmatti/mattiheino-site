from unittest.mock import MagicMock, patch
import pytest

from lib.wayback import fetch_snapshot_html, fetch_image_bytes, WaybackError


@patch("lib.wayback.requests.get")
def test_fetch_snapshot_html_returns_body_on_200(mock_get):
    mock_get.return_value = MagicMock(status_code=200, text="<article>x</article>")
    html = fetch_snapshot_html(
        "https://www.motivationselfmanagement.com/safe-changes/",
        "20200201123456",
    )
    assert "<article>" in html


@patch("lib.wayback.requests.get")
def test_fetch_snapshot_html_raises_on_503(mock_get):
    mock_get.return_value = MagicMock(status_code=503, text="busy")
    with pytest.raises(WaybackError):
        fetch_snapshot_html("https://x.test/", "20200201123456")


@patch("lib.wayback.requests.get")
def test_fetch_image_bytes_uses_im_infix(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200, content=b"\xff\xd8\xff\xd9", headers={}
    )
    data = fetch_image_bytes(
        "https://www.motivationselfmanagement.com/wp-content/uploads/2020/02/x.png",
        "20200201123456",
    )
    assert mock_get.call_args[0][0].startswith(
        "https://web.archive.org/web/20200201123456im_/"
    )
    assert data.startswith(b"\xff\xd8")
