import re
from pathlib import Path

import polib

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "locale" / "zh_Hans" / "LC_MESSAGES" / "django.po"
PLACEHOLDER = re.compile(r"%\([^)]+\)[#0 +\-]?\d*(?:\.\d+)?[a-zA-Z]|\{[^{}]+\}")


def _entries():
    return [entry for entry in polib.pofile(CATALOG) if entry.msgid and not entry.obsolete]


def test_chinese_catalog_has_no_empty_or_fuzzy_entries():
    entries = _entries()
    empty = [entry.msgid for entry in entries if not entry.msgstr]
    fuzzy = [entry.msgid for entry in entries if "fuzzy" in entry.flags]

    assert empty == []
    assert fuzzy == []


def test_chinese_catalog_preserves_format_placeholders():
    mismatches = []

    for entry in _entries():
        source = sorted(PLACEHOLDER.findall(entry.msgid))
        translation = sorted(PLACEHOLDER.findall(entry.msgstr))
        if source != translation:
            mismatches.append((entry.msgid, source, translation))

    assert mismatches == []


def test_chinese_catalog_has_project_metadata():
    catalog = polib.pofile(CATALOG)

    assert catalog.metadata["Project-Id-Version"] == "BrightBean Studio"
    assert catalog.metadata["Language"] == "zh_CN"


def test_technical_and_product_terms_have_context_appropriate_translations():
    translations = {entry.msgid: entry.msgstr for entry in _entries()}

    assert translations["Post"] == "帖子"
    assert translations["P"] == "P"
    assert translations["p20"] == "p20"
    assert translations["p50"] == "p50"
    assert translations["p80"] == "p80"
    assert translations["Crop"] == "裁剪"
