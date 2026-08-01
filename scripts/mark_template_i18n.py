"""Mechanically mark static application template strings for Django gettext.

The scanner respects quoted HTML attributes and skips script, style, and SVG
content. It deliberately leaves text containing Django block tags for manual
conversion because conditionals must be split into separate translation units.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
ATTRIBUTE = re.compile(r'(?P<prefix>\b(?:placeholder|title|aria-label)=)(?P<quote>["\'])(?P<body>.*?)(?P=quote)')
TAG_NAME = re.compile(r"<\s*(?P<closing>/?)\s*(?P<name>[A-Za-z][A-Za-z0-9:_-]*)")
ENGLISH = re.compile(r"[A-Za-z]")
PROTECTED_ELEMENTS = {"script", "style", "svg"}
ALLOWED = {
    "BrightBean", "Brightbean", "Facebook", "Instagram", "LinkedIn",
    "TikTok", "YouTube", "Pinterest", "Threads", "Bluesky", "Mastodon",
    "Google", "GitHub", "API", "OAuth", "URL", "CSV", "PDF",
}


def allowed_literal(text: str) -> bool:
    words = set(re.findall(r"[A-Za-z][A-Za-z0-9.+-]*", text))
    return bool(words) and words.issubset(ALLOWED)


def mark_text(body: str) -> str:
    literal_text = re.sub(r"{{.*?}}", "", body, flags=re.DOTALL)
    literal_text = re.sub(r"{#.*?#}", "", literal_text, flags=re.DOTALL)
    if not ENGLISH.search(literal_text) or "{%" in body:
        return body
    leading = body[: len(body) - len(body.lstrip())]
    trailing = body[len(body.rstrip()) :]
    text = body.strip()
    if not text or allowed_literal(text):
        return body
    return f"{leading}{{% blocktranslate %}}{text}{{% endblocktranslate %}}{trailing}"


def mark_attributes(tag: str) -> str:
    def replace(match: re.Match[str]) -> str:
        body = match.group("body")
        if not ENGLISH.search(body) or "{%" in body or "{{" in body or allowed_literal(body):
            return match.group(0)
        escaped = body.replace("\\", "\\\\").replace("'", "\\'")
        return f'{match.group("prefix")}"{{% translate \'{escaped}\' %}}"'

    return ATTRIBUTE.sub(replace, tag)


def find_tag_end(source: str, start: int) -> int:
    quote: str | None = None
    index = start + 1
    while index < len(source):
        char = source[index]
        if quote:
            if char == quote and source[index - 1] != "\\":
                quote = None
        elif char in {'"', "'"}:
            quote = char
        elif char == ">":
            return index + 1
        index += 1
    return len(source)


def transform(source: str) -> str:
    parts: list[str] = []
    index = 0
    text_start = 0
    protected_depth = 0

    while index < len(source):
        if source.startswith("<!--", index):
            if text_start < index:
                text = source[text_start:index]
                parts.append(text if protected_depth else mark_text(text))
            end = source.find("-->", index + 4)
            end = len(source) if end == -1 else end + 3
            parts.append(source[index:end])
            index = end
            text_start = end
            continue

        if source[index] != "<":
            index += 1
            continue

        if text_start < index:
            text = source[text_start:index]
            parts.append(text if protected_depth else mark_text(text))

        end = find_tag_end(source, index)
        tag = source[index:end]
        match = TAG_NAME.match(tag)
        name = match.group("name").lower() if match else ""
        closing = bool(match and match.group("closing"))

        if closing and name in PROTECTED_ELEMENTS:
            protected_depth = max(0, protected_depth - 1)

        parts.append(tag if protected_depth else mark_attributes(tag))

        if not closing and name in PROTECTED_ELEMENTS and not tag.rstrip().endswith("/>"):
            protected_depth += 1

        index = end
        text_start = end

    if text_start < len(source):
        text = source[text_start:]
        parts.append(text if protected_depth else mark_text(text))

    transformed = "".join(parts)
    if transformed != source and "{% load i18n %}" not in transformed:
        lines = transformed.splitlines(keepends=True)
        insert_at = 1 if lines and lines[0].lstrip().startswith("{% extends") else 0
        lines.insert(insert_at, "{% load i18n %}\n")
        transformed = "".join(lines)
    return transformed


def main() -> None:
    changed = 0
    for path in sorted(TEMPLATES.rglob("*.html")):
        source = path.read_text(encoding="utf-8")
        transformed = transform(source)
        if transformed != source:
            path.write_text(transformed, encoding="utf-8")
            changed += 1
    print(f"Marked {changed} templates")


if __name__ == "__main__":
    main()
