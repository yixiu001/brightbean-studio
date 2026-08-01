# BrightBean Studio Chinese Internationalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Simplified Chinese the default UI language, allow persistent switching to English, and add Chinese counterparts for all six existing Markdown documents without modifying the English originals.

**Architecture:** Use Django's native gettext pipeline, `LocaleMiddleware`, `set_language`, template translation tags, and Python gettext calls. Keep English source strings as msgids, store Simplified Chinese translations in one `zh_Hans` catalog, and expose a POST-based switcher in the shared shell so ordinary and HTMX requests inherit the same language cookie.

**Tech Stack:** Django 5.x i18n, Django templates, HTMX, GNU gettext, pytest/pytest-django, Markdown.

## Global Constraints

- Default language is Simplified Chinese (`zh-hans`); English remains selectable.
- Existing English Markdown files must remain byte-for-byte unchanged.
- Chinese Markdown copies use the `_cn.md` suffix in the same directory.
- Translate application-owned UI and application-owned user messages; do not translate user content or social-platform payloads.
- Do not modify third-party package source code.
- Preserve template variables, format placeholders, code blocks, commands, URLs, API fields, feature IDs, and file paths.
- Do not change business behavior, database schema, layout, or brand styling.

---

### Task 1: Establish the i18n configuration and language endpoint

**Files:**
- Modify: `config/settings/base.py`
- Modify: `config/urls.py`
- Create: `tests/test_i18n.py`

**Interfaces:**
- Produces: `settings.LANGUAGES = (("zh-hans", "简体中文"), ("en", "English"))`
- Produces: `POST /i18n/setlang/` through Django's named URL `set_language`
- Produces: locale discovery through `settings.LOCALE_PATHS`

- [ ] **Step 1: Write failing configuration and language-switch tests**

```python
from django.conf import settings
from django.test import Client
from django.urls import reverse


def test_simplified_chinese_is_default_language():
    assert settings.LANGUAGE_CODE == "zh-hans"
    assert settings.LANGUAGES == (("zh-hans", "简体中文"), ("en", "English"))
    assert "django.middleware.locale.LocaleMiddleware" in settings.MIDDLEWARE


def test_language_switch_sets_cookie_and_returns_to_local_page():
    response = Client().post(reverse("set_language"), {"language": "en", "next": "/"})
    assert response.status_code == 302
    assert response.url == "/"
    assert response.cookies[settings.LANGUAGE_COOKIE_NAME].value == "en"


def test_language_switch_rejects_external_redirect():
    response = Client().post(
        reverse("set_language"),
        {"language": "en", "next": "https://example.com/steal"},
    )
    assert response.status_code == 302
    assert response.url == "/"
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run: `pytest tests/test_i18n.py -q`

Expected: failures for English default, missing LocaleMiddleware, and missing `set_language` route.

- [ ] **Step 3: Add the minimal Django configuration**

In `config/settings/base.py`, place `LocaleMiddleware` immediately after `SessionMiddleware`, set the language values, and register the repository locale directory:

```python
from django.utils.translation import gettext_lazy as _

MIDDLEWARE = [
    # existing middleware before SessionMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # remaining existing middleware
]

LANGUAGE_CODE = "zh-hans"
LANGUAGES = (
    ("zh-hans", _("Simplified Chinese")),
    ("en", _("English")),
)
LOCALE_PATHS = [BASE_DIR / "locale"]
```

In `config/urls.py`, add the official language URLs before application routes:

```python
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    # existing routes
]
```

- [ ] **Step 4: Run the focused tests**

Run: `pytest tests/test_i18n.py -q`

Expected: all tests pass.

- [ ] **Step 5: Commit the configuration slice**

```bash
git add config/settings/base.py config/urls.py tests/test_i18n.py
git commit -m "add Django language configuration"
```

---

### Task 2: Add the global language switcher and language-aware document shell

**Files:**
- Modify: `templates/base.html`
- Modify: `templates/base.html` sidebar block beginning at the `<aside>` near line 277
- Modify: `tests/test_i18n.py`

**Interfaces:**
- Consumes: named URL `set_language` from Task 1
- Produces: a POST form containing `language` and a safe `next` path
- Produces: `<html lang="{{ LANGUAGE_CODE }}">`

- [ ] **Step 1: Locate the single shared navigation insertion point**

Run:

```bash
rg -n "include.*sidebar|sidebar-initial|</aside>|</nav>" templates/base.html templates -g '*.html'
```

Expected: identify the one partial used for authenticated navigation; do not duplicate the switcher across feature pages.

- [ ] **Step 2: Add failing rendering assertions**

Extend `tests/test_i18n.py`:

```python
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.utils import translation


def test_base_shell_uses_active_language_and_has_switcher():
    request = RequestFactory().get("/current/?tab=calendar")
    with translation.override("zh-hans"):
        html = render_to_string("base.html", {"request": request})
    assert '<html lang="zh-hans"' in html
    assert 'action="/i18n/setlang/"' in html
    assert 'name="language"' in html
```

- [ ] **Step 3: Run the focused test and confirm failure**

Run: `pytest tests/test_i18n.py::test_base_shell_uses_active_language_and_has_switcher -q`

Expected: failure because the shell is hard-coded to `lang="en"` and has no switcher.

- [ ] **Step 4: Implement the shell and switcher**

Load i18n in the shared templates and use Django's current-language tag:

```django
{% load static i18n %}
{% get_current_language as LANGUAGE_CODE %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}" style="{% block html_style %}{% endblock %}">
```

Add one compact POST switcher in the shared navigation:

```django
<form action="{% url 'set_language' %}" method="post" class="language-switcher">
  {% csrf_token %}
  <input name="next" type="hidden" value="{{ request.get_full_path }}">
  {% get_current_language as LANGUAGE_CODE %}
  {% if LANGUAGE_CODE == 'zh-hans' %}
    <button type="submit" name="language" value="en" aria-label="{% translate 'Switch to English' %}">English</button>
  {% else %}
    <button type="submit" name="language" value="zh-hans" aria-label="{% translate 'Switch to Simplified Chinese' %}">中文</button>
  {% endif %}
</form>
```

Use existing button/sidebar utility classes so layout and branding do not change.

- [ ] **Step 5: Run focused tests and commit**

Run: `pytest tests/test_i18n.py -q`

```bash
git add templates/base.html templates/components tests/test_i18n.py
git commit -m "add persistent language switcher"
```

---

### Task 3: Mark all application-owned template strings for translation

**Files:**
- Modify: `templates/**/*.html`
- Modify: `apps/**/templates/**/*.html`
- Create: `tests/i18n/test_template_translation_markers.py`

**Interfaces:**
- Consumes: Django template i18n tags
- Produces: English gettext msgids for every application-owned visible label, title, placeholder, confirmation, tooltip, empty state, and ARIA label

- [ ] **Step 1: Create an inventory test for obvious untranslated text**

Create a scanner that inspects project-owned HTML templates, ignores script/style/code/svg blocks and template variables, and reports visible English text or user-facing attributes not contained in `{% translate %}` / `{% blocktranslate %}` constructs. The allowlist must only contain product names, platform names, acronyms, and user-generated examples:

```python
ALLOWED_LITERALS = {
    "BrightBean", "Facebook", "Instagram", "LinkedIn", "TikTok",
    "YouTube", "Pinterest", "Threads", "Bluesky", "Mastodon",
    "Google", "GitHub", "API", "OAuth", "URL", "CSV", "PDF",
}
```

The test must print file and line number for each candidate so omissions can be fixed deterministically.

- [ ] **Step 2: Run the inventory and save the initial failure list**

Run: `pytest tests/i18n/test_template_translation_markers.py -q`

Expected: fail with candidates from the current 163+ templates containing English UI text.

- [ ] **Step 3: Convert shared shells and reusable components first**

Update `templates/base.html`, `templates/components/**/*.html`, and `templates/oauth2_provider/authorize.html` using these rules:

```django
{% load i18n %}
{% translate "Save" %}
{% blocktranslate with workspace_name=workspace.name %}Settings for {{ workspace_name }}{% endblocktranslate %}
<input placeholder="{% translate 'Search posts' %}">
<button aria-label="{% translate 'Dismiss' %}">
```

Never translate CSS classes, Alpine expressions, HTMX attributes, URL names, template variable names, or platform identifiers.

- [ ] **Step 4: Convert templates app-by-app**

Process and re-run the inventory after each directory, in this order:

```text
apps/accounts/templates/
apps/organizations/templates/
apps/workspaces/templates/
apps/members/templates/
apps/onboarding/templates/
apps/composer/templates/
apps/calendar/templates/
apps/approvals/templates/
apps/client_portal/templates/
apps/social_accounts/templates/
apps/media_library/templates/
apps/inbox/templates/
apps/analytics/templates/
apps/notifications/templates/
apps/settings_manager/templates/
apps/credentials/templates/
apps/api_keys/templates/
apps/intelligence/templates/
```

For each directory: add `{% load i18n %}` where needed, mark every application-owned visible string, render the affected template tests, then continue.

- [ ] **Step 5: Verify no obvious template literals remain**

Run:

```bash
pytest tests/i18n/test_template_translation_markers.py -q
python manage.py check
```

Expected: scanner passes and Django reports no template/configuration errors.

- [ ] **Step 6: Commit template markers**

```bash
git add templates apps/*/templates tests/i18n/test_template_translation_markers.py
git commit -m "mark interface templates for translation"
```

---

### Task 4: Mark application-owned Python messages and JavaScript strings

**Files:**
- Modify: `apps/**/*.py`
- Modify: application-owned inline JavaScript in `templates/**/*.html` and `apps/**/templates/**/*.html`
- Create: `tests/i18n/test_python_translation_markers.py`

**Interfaces:**
- Produces: lazy-translated form labels and validation messages
- Produces: runtime-translated view messages, notifications, and API-facing human descriptions
- Produces: template-injected translations for JavaScript UI messages

- [ ] **Step 1: Add a failing Python message inventory**

Scan application Python AST for literal strings passed to user-facing APIs including:

```python
USER_MESSAGE_CALLS = {
    "messages.success", "messages.error", "messages.warning", "messages.info",
    "ValidationError", "forms.CharField", "forms.ChoiceField",
}
```

Also flag model/form `verbose_name`, `help_text`, field `label`, and project-owned notification text that is not wrapped in `_()`.

- [ ] **Step 2: Run the scanner and confirm failure**

Run: `pytest tests/i18n/test_python_translation_markers.py -q`

Expected: fail with current application-owned English messages.

- [ ] **Step 3: Translate definitions and runtime messages correctly**

At module scope use lazy translation:

```python
from django.utils.translation import gettext_lazy as _

title = models.CharField(_("Title"), max_length=255)
raise ValidationError(_("This post cannot be scheduled in the past."))
```

Where a translated string must be resolved immediately, use `gettext`:

```python
from django.utils.translation import gettext as _

messages.success(request, _("Post scheduled successfully."))
```

Do not translate log messages, internal exception diagnostics, API field names, enum stored values, provider payload keys, or audit event identifiers.

- [ ] **Step 4: Replace JavaScript user literals with template-provided translations**

Example:

```django
<script nonce="{{ request.csp_nonce }}">
  const uiMessages = {
    failed: "{% translate 'Something went wrong. Please try again.'|escapejs %}",
    confirmDelete: "{% translate 'Delete this item?'|escapejs %}",
  };
</script>
```

Preserve CSP nonces and do not introduce a new JavaScript build step.

- [ ] **Step 5: Run focused and existing tests**

Run:

```bash
pytest tests/i18n/test_python_translation_markers.py tests/test_i18n.py -q
pytest apps/accounts apps/composer apps/calendar apps/approvals apps/inbox apps/analytics -q
```

Expected: all selected tests pass.

- [ ] **Step 6: Commit Python and JavaScript markers**

```bash
git add apps templates tests/i18n/test_python_translation_markers.py
git commit -m "mark application messages for translation"
```

---

### Task 5: Build and verify the Simplified Chinese message catalog

**Files:**
- Create: `locale/zh_Hans/LC_MESSAGES/django.po`
- Create: `locale/zh_Hans/LC_MESSAGES/django.mo`
- Create: `tests/i18n/test_catalog_completeness.py`

**Interfaces:**
- Consumes: msgids extracted in Tasks 2-4
- Produces: compiled Simplified Chinese runtime translations

- [ ] **Step 1: Extract all application messages**

Run:

```bash
python manage.py makemessages -l zh_Hans --ignore '.venv/*' --ignore 'staticfiles/*'
```

Expected: `django.po` contains source references for templates and Python files.

- [ ] **Step 2: Translate every application-owned msgid**

For every non-empty `msgid`, add a natural Simplified Chinese `msgstr`. Preserve Python-format and brace-format placeholders exactly. Keep product names and social-platform names unchanged unless the established Chinese name is clearer.

- [ ] **Step 3: Add catalog integrity tests**

Use Python's `polib` in a test-only helper if already available; otherwise parse with Django/gettext tooling. Assert:

```python
def test_chinese_catalog_has_no_fuzzy_or_empty_application_entries():
    # Ignore the metadata entry where msgid == "".
    assert untranslated == []
    assert fuzzy == []


def test_format_placeholders_are_preserved():
    assert placeholder_mismatches == []
```

- [ ] **Step 4: Compile and run catalog tests**

Run:

```bash
python manage.py compilemessages
pytest tests/i18n/test_catalog_completeness.py tests/test_i18n.py -q
```

Expected: catalog compiles without placeholder errors; tests pass.

- [ ] **Step 5: Render representative pages in both languages**

Add client tests for login, dashboard, composer, calendar, approvals, inbox, analytics, settings, and onboarding. For each route, request once with `django_language=zh-hans` and once with `django_language=en`; assert 200/expected redirect and assert one known translated label in each response.

- [ ] **Step 6: Commit the catalog**

```bash
git add locale tests/i18n tests/test_i18n.py
git commit -m "add Simplified Chinese message catalog"
```

---

### Task 6: Create Chinese root documentation without changing English files

**Files:**
- Create: `README_cn.md`
- Create: `CONTRIBUTING_cn.md`
- Create: `SECURITY_cn.md`
- Create: `tests/i18n/test_chinese_docs.py`

**Interfaces:**
- Produces: complete Chinese versions of all root Markdown documents

- [ ] **Step 1: Record immutable English document hashes in the test**

Compute SHA-256 for the three English files on the base commit and store the expected digests in `tests/i18n/test_chinese_docs.py`. The test must assert those files retain the same hashes.

- [ ] **Step 2: Add existence and structure tests**

Assert each `_cn.md` file exists, has the same fenced-code-block count as its English source, and contains no translation sentinel such as `TRANSLATION_MISSING`.

- [ ] **Step 3: Translate the three documents**

Translate headings, prose, notes, table prose, and user-facing examples. Preserve commands, environment variables, URLs, badges, code blocks, filenames, paths, API names, and Markdown link destinations.

Add reciprocal language links near the top without modifying the English originals only when the Chinese file can link back to English; do not add links to English files because they must remain unchanged.

- [ ] **Step 4: Run document tests and commit**

Run: `pytest tests/i18n/test_chinese_docs.py -q`

```bash
git add README_cn.md CONTRIBUTING_cn.md SECURITY_cn.md tests/i18n/test_chinese_docs.py
git commit -m "add Chinese root documentation"
```

---

### Task 7: Create Chinese development specifications without changing English files

**Files:**
- Create: `development_specs/architecture_cn.md`
- Create: `development_specs/feature-spec-social-media-management-v2_cn.md`
- Create: `development_specs/meta-analytics-manual-tests_cn.md`
- Modify: `tests/i18n/test_chinese_docs.py`

**Interfaces:**
- Produces: complete Chinese versions of all Markdown files under `development_specs/`

- [ ] **Step 1: Add base hashes and structural assertions for all three specifications**

Record the base-commit SHA-256 values. Assert source hashes remain unchanged, heading counts match, fenced-code-block counts match, and feature IDs `F-1.1` through `F-8.7` remain present in the large feature specification.

- [ ] **Step 2: Translate `meta-analytics-manual-tests.md`**

Translate headings and validation prose. Preserve Meta Graph API paths, metric names, IDs, tokens, and code fences exactly.

- [ ] **Step 3: Translate `architecture.md`**

Translate architecture explanations, tables, warnings, deployment instructions, and security/backup descriptions. Preserve tree diagrams, shell commands, environment variables, class/function names, URLs, prices, and provider identifiers.

- [ ] **Step 4: Translate `feature-spec-social-media-management-v2.md` in numbered sections**

Translate Product Positioning, Information Architecture, F-1 through F-8, complete data model, build phases, and technical requirements. Preserve every feature ID, model/field identifier, enum value, API scope, code block, acceptance-criteria checkbox structure, and dependency reference.

- [ ] **Step 5: Run structural tests and inspect the large diff**

Run:

```bash
pytest tests/i18n/test_chinese_docs.py -q
git diff --check
```

Expected: source hashes unchanged, all six Chinese documents exist, structure checks pass, and no whitespace errors.

- [ ] **Step 6: Commit translated specifications**

```bash
git add development_specs/*_cn.md tests/i18n/test_chinese_docs.py
git commit -m "add Chinese development specifications"
```

---

### Task 8: Full verification and delivery

**Files:**
- Modify only files required to fix verification failures within the approved scope

**Interfaces:**
- Produces: verified branch ready for a Draft PR to `main`

- [ ] **Step 1: Run static Django and translation checks**

```bash
python manage.py check
python manage.py makemessages -l zh_Hans --no-obsolete --ignore '.venv/*' --ignore 'staticfiles/*'
python manage.py compilemessages
git diff --check
```

- [ ] **Step 2: Run all internationalization tests**

Run: `pytest tests/i18n tests/test_i18n.py -q`

Expected: all pass.

- [ ] **Step 3: Run the complete regression suite**

Run: `pytest -q`

Expected: all tests pass. If a dependency or external service prevents a test, record the exact failing command and reason; do not report the suite as passing.

- [ ] **Step 4: Verify English sources are unchanged**

```bash
git diff main...HEAD -- README.md CONTRIBUTING.md SECURITY.md \
  development_specs/architecture.md \
  development_specs/feature-spec-social-media-management-v2.md \
  development_specs/meta-analytics-manual-tests.md
```

Expected: no output.

- [ ] **Step 5: Review translation coverage**

Run both marker scanners and catalog completeness tests again. Manually inspect representative Chinese and English pages for broken variables, untranslated controls, overflow in sidebar/buttons, and language persistence after HTMX navigation.

- [ ] **Step 6: Commit any verification-only corrections**

```bash
git add <only-the-files-corrected-during-verification>
git commit -m "fix Chinese localization verification issues"
```

Skip this commit when no corrections are needed.

- [ ] **Step 7: Push the branch and open a Draft PR**

Push `agent/i18n-zh-cn` and open a Draft PR targeting `yixiu001/brightbean-studio:main`. The PR body must list UI coverage, documentation coverage, default-language behavior, tests executed, and any known third-party translation limitations.
