from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import translation


def test_simplified_chinese_is_default_language():
    assert settings.LANGUAGE_CODE == "zh-hans"


def test_supported_languages_include_chinese_and_english():
    assert settings.LANGUAGES == (("zh-hans", "简体中文"), ("en", "English"))


def test_locale_middleware_runs_after_session_middleware():
    session_index = settings.MIDDLEWARE.index("django.contrib.sessions.middleware.SessionMiddleware")
    locale_index = settings.MIDDLEWARE.index("django.middleware.locale.LocaleMiddleware")
    assert locale_index == session_index + 1


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


def test_base_shell_uses_active_language_and_has_switcher():
    request = RequestFactory().get("/current/?tab=calendar")
    request.user = AnonymousUser()

    with translation.override("zh-hans"):
        html = render_to_string("base.html", {}, request=request)

    assert '<html lang="zh-hans"' in html
    assert 'action="/i18n/setlang/"' in html
    assert 'name="language"' in html
    assert 'value="en"' in html
