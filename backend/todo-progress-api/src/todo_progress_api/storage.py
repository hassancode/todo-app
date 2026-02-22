from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from .models import ProgressEvent, ProgressEventCreate

_events: list[ProgressEvent] = []


def record_event(data: ProgressEventCreate) -> ProgressEvent:
    event = ProgressEvent(
        id=uuid4(),
        task_id=data.task_id,
        event_type=data.event_type,
        old_status=data.old_status,
        new_status=data.new_status,
        timestamp=datetime.now(timezone.utc),
    )
    _events.append(event)
    return event


def list_events() -> list[ProgressEvent]:
    return list(_events)


def get_events_for_task(task_id: UUID) -> list[ProgressEvent]:
    return [e for e in _events if e.task_id == task_id]
