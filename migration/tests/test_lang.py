import pytest
from lib.lang import infer_lang


def test_clear_finnish_categories_returns_fi():
    assert infer_lang(categories=["Ilmahygienia", "Varautuminen"], body="") == "fi"


def test_clear_english_categories_returns_en():
    assert infer_lang(categories=["Complex systems"], body="") == "en"


def test_no_categories_falls_back_to_body_heuristic_fi():
    body = "Tämä on suomenkielinen teksti, jossa on ääkkösiä ja muita merkkejä."
    assert infer_lang(categories=[], body=body) == "fi"


def test_no_categories_falls_back_to_body_heuristic_en():
    body = "This is an English-language post about behaviour change and uncertainty."
    assert infer_lang(categories=[], body=body) == "en"


def test_finnish_chars_dominate_short_body_returns_fi():
    body = "Pää ja ääni."
    assert infer_lang(categories=[], body=body) == "fi"


def test_mixed_categories_picks_more_frequent():
    # "Käyttäytymismuutos" is the FI side; should win
    assert infer_lang(categories=["Käyttäytymismuutos", "Käyttäytymismuutos", "Decision-making"], body="") == "fi"
