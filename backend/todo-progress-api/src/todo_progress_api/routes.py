from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter

from .models import ProgressEvent, ProgressEventCreate
from . import storage

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/", response_model=ProgressEvent, status_code=201)
async def record_event(data: ProgressEventCreate) -> ProgressEvent:
    return storage.record_event(data)


@router.get("/", response_model=list[ProgressEvent])
async def list_events() -> list[ProgressEvent]:
    return storage.list_events()


@router.get("/{task_id}", response_model=list[ProgressEvent])
async def get_events_for_task(task_id: UUID) -> list[ProgressEvent]:
    return storage.get_events_for_task(task_id)
