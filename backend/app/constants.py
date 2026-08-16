"""Single source of truth for enum-like status values across the API."""

RECORD_STATUSES = ("raw", "edited", "verified")
DATASET_STATUSES = ("draft", "published", "archived")
USER_ROLES = ("admin", "editor", "viewer")
WEBHOOK_EVENTS = ("create", "update", "delete")
