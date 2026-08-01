import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = {
    "README.md": "eda679498b85c764fd1d38af1d885f84fd76df81ebcb28fb84fb6329d9c7e61c",
    "CONTRIBUTING.md": "e3235b8b37ff721d6981b505f72a0a6572dbfd0183da8a0b2f6ede12d2dab4d1",
    "SECURITY.md": "2b48f365af5f6855ea48d1f8340673d5c16c47e445589de8d09c571521a73ab1",
    "development_specs/architecture.md": "21b1c34ae214ddc0a28e2602790c943a00e5f8944491c0443d35552616cea785",
    "development_specs/feature-spec-social-media-management-v2.md": "493e5f5e697a3896fbe38b4a8c9afaea4235d18376a8369dc871c13ebd9a7b1f",
    "development_specs/meta-analytics-manual-tests.md": "e14fb21fc14a6520388764715e11212c108ccd838f988554b634cbfa752b14ec",
}


def chinese_path(source: Path) -> Path:
    return source.with_name(f"{source.stem}_cn{source.suffix}")


def test_english_markdown_sources_are_unchanged():
    mismatches = []
    for relative_path, expected_hash in DOCUMENTS.items():
        source = ROOT / relative_path
        actual_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            mismatches.append((relative_path, expected_hash, actual_hash))
    assert mismatches == []


def test_every_english_document_has_a_complete_chinese_counterpart():
    missing = []
    structural_mismatches = []

    for relative_path in DOCUMENTS:
        source = ROOT / relative_path
        translated = chinese_path(source)
        if not translated.exists():
            missing.append(str(translated.relative_to(ROOT)))
            continue

        source_text = source.read_text(encoding="utf-8")
        translated_text = translated.read_text(encoding="utf-8")
        if source_text.count("```") != translated_text.count("```"):
            structural_mismatches.append(f"{relative_path}: fenced code block count")
        if source_text.count("\n#") != translated_text.count("\n#"):
            structural_mismatches.append(f"{relative_path}: heading count")
        if "TRANSLATION_MISSING" in translated_text:
            structural_mismatches.append(f"{relative_path}: translation sentinel")

    assert missing == []
    assert structural_mismatches == []
