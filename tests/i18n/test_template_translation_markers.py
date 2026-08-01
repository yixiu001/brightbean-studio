from pathlib import Path

from django.template import engines

from scripts.mark_template_i18n import transform

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"


def test_static_template_strings_are_marked_for_translation():
    unmarked: list[str] = []

    for path in sorted(TEMPLATES.rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        if transform(source) != source:
            unmarked.append(str(path.relative_to(ROOT)))

    assert unmarked == [], "Templates with unmarked static UI strings:\n" + "\n".join(unmarked)


def test_all_application_templates_compile():
    backend = engines["django"]
    failures: list[str] = []

    for path in sorted(TEMPLATES.rglob("*.html")):
        template_name = str(path.relative_to(TEMPLATES))
        try:
            backend.get_template(template_name)
        except Exception as exc:  # pragma: no cover - assertion reports exact template
            failures.append(f"{template_name}: {exc}")

    assert failures == [], "Templates that failed to compile:\n" + "\n".join(failures)
