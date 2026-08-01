"""Localized, presentation-only labels for publish-page timezones."""

from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


TIMEZONE_LABELS = {
    "US/Eastern": _("Eastern"),
    "US/Central": _("Central"),
    "US/Mountain": _("Mountain"),
    "US/Pacific": _("Pacific"),
    "UTC": _("UTC"),
    "Europe/London": _("London"),
    "Europe/Paris": _("Paris"),
    "Europe/Berlin": _("Berlin"),
    "Europe/Amsterdam": _("Amsterdam"),
    "Asia/Tokyo": _("Tokyo"),
    "Asia/Shanghai": _("Shanghai"),
    "Asia/Kolkata": _("Kolkata"),
    "Asia/Dubai": _("Dubai"),
    "Australia/Sydney": _("Sydney"),
    "Pacific/Auckland": _("Auckland"),
    "America/Sao_Paulo": _("Sao Paulo"),
    "America/Toronto": _("Toronto"),
    "America/Chicago": _("Chicago"),
    "America/Denver": _("Denver"),
    "America/Los_Angeles": _("Los Angeles"),
    "America/New_York": _("New York"),
}


@register.filter
def timezone_label(value: str) -> str:
    """Return a localized display label while preserving the IANA identifier."""
    identifier = str(value or "")
    return TIMEZONE_LABELS.get(identifier) or identifier.rsplit("/", maxsplit=1)[-1].replace("_", " ")
