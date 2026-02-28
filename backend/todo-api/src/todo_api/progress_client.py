from __future__ import annotations

import logging
import os
from uuid import UUID

import httpx

PROGRESS_API_URL = os.getenv("PROGRESS_API_URL", "http://127.0.0.1:8001")

logger = logging.getLogger(__name__)


async def record_event(
    task_id: UUID,
    event_type: str,
    old_status: str | None = None,
    new_status: str | None = None,
) -> None:
    payload = {
        "task_id": str(task_id),
        "event_type": event_type,
        "old_status": old_status,
        "new_status": new_status,
    }
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{PROGRESS_API_URL}/progress", json=payload, timeout=5.0)
    except httpx.HTTPError as exc:
        logger.warning("Failed to record progress event: %s", exc)
