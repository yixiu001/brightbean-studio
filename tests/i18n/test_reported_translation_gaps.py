from types import SimpleNamespace

import pytest
from django.template import Context, engines
from django.test import RequestFactory
from django.utils.translation import override

from apps.calendar.templatetags.timezone_labels import timezone_label
from apps.notifications.models import EventType
from apps.workspaces.models import Workspace


def _render(template_name: str, context: dict) -> str:
    workspace = context["workspace"]
    request = RequestFactory().get("/")
    request.workspace = workspace
    request.user = SimpleNamespace(
        is_authenticated=True,
        avatar=None,
        name="Tester",
        email="tester@example.com",
    )
    return engines["django"].engine.get_template(template_name).render(
        Context({**context, "request": request, "user": request.user})
    )


def test_archiving_guidance_renders_in_chinese_for_a_non_archivable_workspace():
    """Catches the archive heading or last-workspace warning being shown in English."""
    workspace = SimpleNamespace(
        id="00000000-0000-0000-0000-000000000001",
        is_archived=False,
        icon=None,
        name="Team",
    )

    with override("zh-hans"):
        rendered = _render(
            "workspaces/settings.html",
            {
                "workspace": workspace,
                "is_owner_or_manager": True,
                "can_archive": False,
                "can_delete": False,
            },
        )

    assert "归档此工作区" in rendered
    assert "无法归档组织中的最后一个活跃工作区" in rendered
    assert "Archive this workspace" not in rendered
    assert "You cannot archive the last active workspace in the organization." not in rendered


def test_publish_tab_labels_render_in_chinese():
    """Catches publish list tabs that remain visible in English."""
    with override("zh-hans"):
        rendered = _render(
            "calendar/partials/publish_list_shell.html",
            {
                "queue_count": 1,
                "drafts_count": 1,
                "approvals_count": 1,
                "sent_count": 1,
                "timezone_choices": [],
                "initial_tab_template": "calendar/partials/publish_queue.html",
                "platform_posts": [],
                "has_connected_accounts": True,
                "workspace": SimpleNamespace(id="00000000-0000-0000-0000-000000000001"),
            },
        )

    for label in ("队列", "草稿", "审批", "已发布"):
        assert label in rendered
    for label in ("Queue", "Drafts", "Approvals", "Sent"):
        assert label not in rendered


def test_notification_event_choice_label_is_localized_without_changing_value():
    """Catches notification preference event labels remaining in English."""
    with override("zh-hans"):
        assert str(EventType.POST_SUBMITTED.label) == "帖子已提交审批"
        assert EventType.POST_SUBMITTED.value == "post_submitted"

    with override("en"):
        assert str(EventType.POST_SUBMITTED.label) == "Post submitted for approval"


def test_timezone_label_is_localized_and_unknown_identifiers_have_a_safe_fallback():
    """Catches publish timezone names showing raw IANA identifiers to users."""
    with override("zh-hans"):
        assert timezone_label("Asia/Shanghai") == "上海"

    with override("en"):
        assert timezone_label("Asia/Shanghai") == "Shanghai"

    assert timezone_label("Etc/Custom_Zone") == "Custom Zone"


@pytest.mark.parametrize(
    "template_name",
    [
        "calendar/partials/publish_list_shell.html",
        "calendar/partials/publish_calendar_shell.html",
    ],
)
def test_publish_timezone_options_keep_iana_values_and_localize_workspace_suffix(template_name):
    """Catches localized labels accidentally changing the timezone sent to the server."""
    workspace = SimpleNamespace(id="00000000-0000-0000-0000-000000000001")

    with override("zh-hans"):
        rendered = _render(
            template_name,
            {
                "queue_count": 0,
                "drafts_count": 0,
                "approvals_count": 0,
                "sent_count": 0,
                "timezone_choices": ["Asia/Shanghai"],
                "display_timezone": "Asia/Shanghai",
                "workspace_timezone": "Asia/Shanghai",
                "initial_tab_template": "calendar/partials/publish_queue.html",
                "platform_posts": [],
                "has_connected_accounts": True,
                "workspace": workspace,
            },
        )

    assert 'value="Asia/Shanghai"' in rendered
    assert ">上海 （工作区）</option>" in rendered


def test_calendar_document_title_renders_in_chinese():
    """Catches the browser title retaining the hard-coded English Publish label."""
    workspace = SimpleNamespace(
        id="00000000-0000-0000-0000-000000000001",
        name="Team",
        icon=None,
    )

    with override("zh-hans"):
        rendered = _render(
            "calendar/calendar.html",
            {
                "workspace": workspace,
                "mode": "list",
                "timezone_choices": [],
                "initial_tab_template": "calendar/partials/publish_queue.html",
                "platform_posts": [],
                "has_connected_accounts": True,
            },
        )

    assert "<title>发布 - Team - Brightbean</title>" in rendered
    assert "<title>Publish - Team - Brightbean</title>" not in rendered


def test_workspace_approval_mode_guidance_renders_in_chinese():
    """Catches conditional approval labels and descriptions bypassing gettext."""
    workspace = SimpleNamespace(
        id="00000000-0000-0000-0000-000000000001",
        name="Team",
        icon=None,
        approval_workflow_mode="none",
    )

    with override("zh-hans"):
        rendered = _render(
            "workspaces/approvals_settings.html",
            {
                "workspace": workspace,
                "is_owner_or_manager": True,
                "approval_modes": Workspace.ApprovalWorkflowMode,
            },
        )

    for text in ("无需审批", "可选审批", "必须内部审核", "内部审核 + 客户审批"):
        assert text in rendered
    assert "任何拥有发布权限的人都可以直接安排或发布。" in rendered
    assert "No approvals" not in rendered
    assert "Anyone with publishing rights can schedule or publish directly." not in rendered


def test_publish_approval_dynamic_labels_render_as_localized_javascript():
    """Catches Alpine-generated selection and rejection labels staying in English."""
    workspace = SimpleNamespace(id="00000000-0000-0000-0000-000000000001")

    with override("zh-hans"):
        rendered = _render(
            "calendar/partials/publish_approvals.html",
            {
                "workspace": workspace,
                "posts": [],
                "can_approve": True,
                "status_filter": "all",
                "approval_filter_qs": "",
            },
        )

    for text in ("全部", "待审核", "已选择", "拒绝", "帖子"):
        assert text in rendered
    for text in ("' selected'", "'Reject '", "' posts'", "' post'"):
        assert text not in rendered


def test_media_library_javascript_messages_render_in_chinese():
    """Catches client-only upload and duration messages bypassing gettext."""
    workspace = SimpleNamespace(
        id="00000000-0000-0000-0000-000000000001",
        name="Team",
        icon=None,
    )

    with override("zh-hans"):
        library = _render(
            "media_library/library_index.html",
            {
                "workspace": workspace,
                "max_bulk_upload": 10,
                "assets": [],
            },
        )
        editor = _render(
            "media_library/asset_edit.html",
            {
                "workspace": workspace,
                "asset": SimpleNamespace(
                    id="00000000-0000-0000-0000-000000000002",
                    original_filename="clip.mp4",
                    file_type="video",
                    duration_seconds=10,
                    mime_type="video/mp4",
                    file=SimpleNamespace(url="/media/clip.mp4"),
                ),
                "is_shared_library": False,
            },
        )

    assert "上传失败" in library
    assert "网络错误" in library
    assert "Upload failed" not in library
    assert "Network error" not in library
    assert "时长：" in editor
    assert "Duration:" not in editor
