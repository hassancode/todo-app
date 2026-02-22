from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class EventType(str, Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"


class ProgressEventCreate(BaseModel):
    task_id: UUID
    event_type: EventType
    old_status: str | None = None
    new_status: str | None = None


class ProgressEvent(BaseModel):
    id: UUID
    task_id: UUID
    event_type: EventType
    old_status: str | None
    new_status: str | None
    timestamp: datetime
