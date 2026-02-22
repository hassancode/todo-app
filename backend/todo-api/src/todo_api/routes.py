from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Response

from .models import Task, TaskCreate, TaskUpdate
from .progress_client import record_event
from . import storage

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=Task, status_code=201)
async def create_task(data: TaskCreate) -> Task:
    task = storage.create_task(data)
    await record_event(task.id, "created", None, task.status.value)
    return task


@router.get("/", response_model=list[Task])
async def list_tasks() -> list[Task]:
    return storage.list_tasks()


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: UUID) -> Task:
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: UUID, data: TaskUpdate) -> Task:
    old = storage.get_task(task_id)
    if old is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task = storage.update_task(task_id, data)
    await record_event(task.id, "updated", old.status.value, task.status.value)
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID) -> Response:
    task = storage.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    storage.delete_task(task_id)
    await record_event(task_id, "deleted", task.status.value, None)
    return Response(status_code=204)
