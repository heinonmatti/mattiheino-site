from lib.pages import disposition_for, PageDisposition


def test_disposition_for_known_slug_returns_import_as_draft():
    d = disposition_for("johdatus-kayttaytymisarkkitehtuuriin")
    assert d.action == "import"
    assert d.draft is True
    assert d.collection == "posts"


def test_disposition_for_10_taitoa_same():
    d = disposition_for("10-taitoa")
    assert d.action == "import"
    assert d.draft is True
    assert d.collection == "posts"


def test_disposition_for_yhteistyon_manifesti_same():
    d = disposition_for("yhteistyon-manifesti")
    assert d.action == "import"
    assert d.draft is True


def test_disposition_for_tervetuloa_returns_skip():
    d = disposition_for("tervetuloa")
    assert d.action == "skip"


def test_disposition_for_unknown_returns_skip_with_reason():
    d = disposition_for("research-the-academic-stuff")
    assert d.action == "skip"
    assert d.reason
