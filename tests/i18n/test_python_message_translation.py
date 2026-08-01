import ast
from pathlib import Path

import pytest
from django.utils.translation import override

ROOT = Path(__file__).resolve().parents[2]
APPS = ROOT / "apps"
MESSAGE_METHODS = {"success", "error", "warning", "info"}
TOAST_FUNCTIONS = {"toast_response", "_toast_response"}


def _is_literal(node: ast.AST) -> bool:
    return isinstance(node, (ast.Constant, ast.JoinedStr)) and (
        not isinstance(node, ast.Constant) or isinstance(node.value, str)
    )


def test_direct_user_messages_are_marked_for_translation():
    """Catches direct message/toast literals that bypass the active locale."""
    failures: list[str] = []

    for path in sorted(APPS.rglob("*.py")):
        if "tests" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "messages"
                and node.func.attr in MESSAGE_METHODS
                and len(node.args) >= 2
                and _is_literal(node.args[1])
            ):
                failures.append(f"{path.relative_to(ROOT)}:{node.lineno}")

            if isinstance(node.func, ast.Name) and node.func.id in TOAST_FUNCTIONS:
                for keyword in node.keywords:
                    if keyword.arg in {"title", "body"} and _is_literal(keyword.value):
                        failures.append(f"{path.relative_to(ROOT)}:{node.lineno}:{keyword.arg}")

    assert failures == [], "Untranslated direct user messages:\n" + "\n".join(failures)


def test_dynamic_workspace_message_uses_named_placeholder_translation():
    """Catches interpolating a workspace name before gettext can translate the sentence."""
    from django.utils.translation import gettext

    with override("zh-hans"):
        message = gettext('Workspace "%(workspace)s" has been archived.') % {"workspace": "Alpha"}

    assert message == '工作区“Alpha”已归档。'


def test_oauth_page_warning_with_arrow_is_translated():
    """Catches source escapes producing a gettext key different from the runtime string."""
    from django.utils.translation import gettext

    source = (
        "No LinkedIn Company Pages were found for your account. "
        "Only Company Pages you administer can be connected — "
        "personal profiles connect via the LinkedIn (Personal) option. "
        "If you expected to see a Page, ask the page owner to grant "
        "you Admin access in LinkedIn → Admin tools → Manage admins, then reconnect."
    )

    with override("zh-hans"):
        message = gettext(source)

    assert message.startswith("未找到 LinkedIn 公司主页。")


def _tree(relative_path: str) -> ast.Module:
    path = ROOT / relative_path
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_indirect_api_key_validation_messages_are_marked_for_translation():
    """Catches literals stored in an errors variable before messages.error displays them."""
    failures: list[int] = []

    for node in ast.walk(_tree("apps/api_keys/views.py")):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "append"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "errors"
            and node.args
            and _is_literal(node.args[0])
        ):
            failures.append(node.lineno)

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in {
            "_parse_expires_at",
            "_resolve_account_allowlist",
        }:
            for child in ast.walk(node):
                if not isinstance(child, ast.Return) or not isinstance(child.value, ast.Tuple):
                    continue
                if any(_is_literal(element) for element in child.value.elts):
                    failures.append(child.lineno)

    assert failures == [], f"Untranslated indirect API-key errors at lines: {sorted(set(failures))}"


def test_client_portal_response_titles_and_bodies_are_marked_for_translation():
    """Catches literals passed through _portal_response before reaching toast_response."""
    failures: list[str] = []

    for node in ast.walk(_tree("apps/client_portal/views.py")):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "_portal_response":
            continue
        for keyword in node.keywords:
            if keyword.arg in {"title", "body"} and _is_literal(keyword.value):
                failures.append(f"{node.lineno}:{keyword.arg}")

    assert failures == [], "Untranslated client-portal responses: " + ", ".join(failures)


def test_approval_value_error_sources_are_marked_for_translation():
    """Catches approval service validation errors that views expose through str(error)."""
    failures: list[int] = []

    for node in ast.walk(_tree("apps/approvals/services.py")):
        if (
            isinstance(node, ast.Raise)
            and isinstance(node.exc, ast.Call)
            and isinstance(node.exc.func, ast.Name)
            and node.exc.func.id == "ValueError"
            and node.exc.args
            and _is_literal(node.exc.args[0])
        ):
            failures.append(node.lineno)

    assert failures == [], f"Untranslated approval ValueError messages at lines: {failures}"


def test_approval_validation_error_resolves_in_chinese():
    """Catches lazy or immediate gettext not resolving before a ValueError is displayed."""
    from apps.approvals.services import request_changes

    with override("zh-hans"), pytest.raises(ValueError) as exc_info:
        request_changes(None, None, None, "")

    assert str(exc_info.value) == "请求修改时必须填写评论。"
