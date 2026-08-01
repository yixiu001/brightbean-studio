# Chinese Internationalization Follow-up Design

## Goal

Complete the Chinese translations for the three user-reported surfaces without changing stored business data or timezone identifiers:

1. Workspace archive and deletion guidance.
2. Notification event-type filters.
3. Publish tabs and timezone display labels.

## Scope

### Workspace settings

Mark every conditional archive, restore, and deletion sentence in `templates/workspaces/settings.html` for Django template translation. Both Chinese and English modes must retain the same conditions and actions.

### Notification event types

Wrap the human-readable labels in `apps/notifications/models.py` with `gettext_lazy`. Stored values such as `post_submitted` and existing database rows remain unchanged. The notification history and preference views continue consuming `EventType.choices`.

### Publish navigation

Mark the visible `Queue`, `Drafts`, `Approvals`, and `Sent` tab labels for translation. Counts and HTMX/Alpine tab identifiers remain unchanged.

### Timezone labels

Keep IANA timezone values such as `Asia/Shanghai` and `US/Eastern` unchanged for requests, filtering, and date conversion. Add a presentation-only mapping that returns localized labels for the common publish-page timezone list. Translate the workspace suffix separately.

The Chinese labels will use familiar city or region names, while English mode will preserve the current concise labels. `UTC` remains `UTC` in both languages.

## Data and compatibility

- No existing business data is translated or rewritten.
- Notification choice values remain stable.
- Timezone query-string values remain stable.
- Database migrations are not required for runtime behavior; any migration generated solely from translated choice metadata should be avoided.

## Testing

Tests must prove that:

- the workspace conditional messages render in Chinese;
- notification choice labels resolve in Chinese while their stored values remain unchanged;
- publish tabs render in Chinese;
- timezone option values remain valid IANA identifiers while their visible labels switch languages;
- English rendering remains available;
- the translation catalog has no empty or fuzzy entries and all affected templates compile.

## Out of scope

- Translating user-entered workspace names, notification bodies, post titles, emails, or account names.
- Renaming social-network brands.
- Changing the complete timezone database or timezone conversion logic.
- General Django admin model-label translation outside the three reported pages.
