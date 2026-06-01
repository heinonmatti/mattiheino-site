from pathlib import Path
from lib.dead_images import DeadImageRow, write_worksheet


def test_write_worksheet_groups_by_collection(tmp_path):
    rows = [
        DeadImageRow(collection="posts", slug="muutoskartta", paragraph=3,
                     original="http://daringtodo.com/x.jpg", alt="Sitku"),
        DeadImageRow(collection="applied-musings", slug="antihauras", paragraph=1,
                     original="http://e.com/y.png", alt="X"),
    ]
    out = tmp_path / "dead.md"
    write_worksheet(out, rows)
    text = out.read_text(encoding="utf-8")
    assert "## posts" in text
    assert "## applied-musings" in text
    assert "muutoskartta" in text
    assert "antihauras" in text


def test_write_worksheet_emits_checkbox_per_row(tmp_path):
    rows = [DeadImageRow(collection="posts", slug="x", paragraph=1, original="u", alt="a")]
    out = tmp_path / "dead.md"
    write_worksheet(out, rows)
    text = out.read_text(encoding="utf-8")
    assert "- [ ]" in text
