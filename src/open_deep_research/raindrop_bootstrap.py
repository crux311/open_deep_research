"""Optional Raindrop Workshop setup for local debugging."""

from __future__ import annotations

import logging
import os
from functools import lru_cache
from typing import Any

logger = logging.getLogger(__name__)


def _enabled(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


@lru_cache(maxsize=1)
def get_raindrop() -> Any | None:
    """Initialize Raindrop once when a local Workshop or write key is configured."""
    if _enabled(os.getenv("RAINDROP_DISABLED")):
        return None

    local_debugger = os.getenv("RAINDROP_LOCAL_DEBUGGER")
    write_key = os.getenv("RAINDROP_WRITE_KEY")

    if not local_debugger and not write_key:
        return None

    try:
        import raindrop.analytics as raindrop
    except Exception as exc:  # pragma: no cover - defensive optional integration
        logger.warning("Raindrop SDK is not available: %s", exc)
        return None

    try:
        raindrop.init(
            api_key=write_key,
            local_workshop_url=local_debugger,
            tracing_enabled=bool(write_key),
            auto_instrument=True,
        )
    except Exception as exc:  # pragma: no cover - tracing must never break agent runs
        logger.warning("Raindrop initialization failed: %s", exc)
        return None

    return raindrop


def start_interaction(
    *,
    user_id: str,
    event: str,
    input_text: str,
    properties: dict[str, Any] | None = None,
    convo_id: str | None = None,
) -> str | None:
    """Start a local Workshop-visible interaction if Raindrop is configured."""
    raindrop = get_raindrop()
    if raindrop is None:
        return None

    try:
        interaction = raindrop.begin(
            user_id=user_id,
            event=event,
            input=input_text,
            properties=properties or {},
            convo_id=convo_id,
        )
        return getattr(interaction, "event_id", None) or getattr(interaction, "_event_id", None)
    except Exception as exc:  # pragma: no cover - observability should be non-fatal
        logger.debug("Raindrop begin failed: %s", exc)
        return None


def finish_interaction(event_id: str | None, *, output: str) -> None:
    """Finish a Raindrop interaction and flush events for Workshop."""
    if not event_id:
        return

    raindrop = get_raindrop()
    if raindrop is None:
        return

    try:
        raindrop.resume_interaction(event_id).finish(output=output)
        raindrop.flush()
    except Exception as exc:  # pragma: no cover - observability should be non-fatal
        logger.debug("Raindrop finish failed: %s", exc)
