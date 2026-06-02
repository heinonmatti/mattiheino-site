import pytest
from pathlib import Path
from lib.categories import load_mapping, categories_to_tags


def test_load_mapping_parses_simple_pairs(tmp_path):
    f = tmp_path / "map.txt"
    f.write_text("Complex systems = complex-systems\nKäyttäytymismuutos = behaviour-change\n", encoding="utf-8")
    m = load_mapping(f)
    assert m["complex systems"] == "complex-systems"
    assert m["käyttäytymismuutos"] == "behaviour-change"


def test_load_mapping_ignores_blank_and_comment_lines(tmp_path):
    f = tmp_path / "map.txt"
    f.write_text("# comment\n\nA = a\n# another\nB = b\n", encoding="utf-8")
    m = load_mapping(f)
    assert m == {"a": "a", "b": "b"}


def test_categories_to_tags_resolves_known():
    m = {"complex systems": "complex-systems", "uncategorized": "uncategorised"}
    assert categories_to_tags(["Complex systems", "Uncategorized"], m) == ["complex-systems", "uncategorised"]


def test_categories_to_tags_unknown_falls_back_to_slug():
    m = {"complex systems": "complex-systems"}
    assert categories_to_tags(["Behaviour Change"], m) == ["behaviour-change"]


def test_categories_to_tags_empty_returns_uncategorised():
    m = {}
    assert categories_to_tags([], m) == ["uncategorised"]


def test_categories_to_tags_dedupes():
    m = {}
    assert categories_to_tags(["Foo", "foo", "FOO"], m) == ["foo"]


def test_categories_to_tags_skip_sentinel_drops_category(tmp_path):
    f = tmp_path / "m.txt"
    f.write_text("º Data punk (English) = (skip)\nComplex systems = complex-systems\n", encoding="utf-8")
    m = load_mapping(f)
    assert categories_to_tags(["º Data punk (English)", "Complex systems"], m) == ["complex-systems"]


def test_categories_to_tags_all_skipped_falls_back_to_uncategorised(tmp_path):
    f = tmp_path / "m.txt"
    f.write_text("Uncategorized = (skip)\n", encoding="utf-8")
    m = load_mapping(f)
    assert categories_to_tags(["Uncategorized"], m) == ["uncategorised"]


def test_categories_to_tags_normalises_nbsp_in_lookup(tmp_path):
    # WP exports use NBSP (U+00A0) between glyphs like the masculine ordinal
    # indicator and the next word. Mapping written with a regular space must
    # still match the category as read from XML.
    f = tmp_path / "m.txt"
    f.write_text("º Data punk (English) = (skip)\n", encoding="utf-8")
    m = load_mapping(f)
    xml_form = "º Data punk (English)"  # NBSP between º and Data
    assert categories_to_tags([xml_form], m) == ["uncategorised"]
