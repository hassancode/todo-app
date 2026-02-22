from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from .models import Task, TaskCreate, TaskStatus, TaskUpdate

_tasks: dict[UUID, Task] = {}


def create_task(data: TaskCreate) -> Task:
    now = datetime.now(timezone.utc)
    task = Task(
        id=uuid4(),
        title=data.title,
        description=data.description,
        status=TaskStatus.pending,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def list_tasks() -> list[Task]:
    return list(_tasks.values())


def get_task(task_id: UUID) -> Task | None:
    return _tasks.get(task_id)


def update_task(task_id: UUID, data: TaskUpdate) -> Task | None:
    task = _tasks.get(task_id)
    if task is None:
        return None
    updates = data.model_dump(exclude_none=True)
    updates["updated_at"] = datetime.now(timezone.utc)
    task = task.model_copy(update=updates)
    _tasks[task_id] = task
    return task


def delete_task(task_id: UUID) -> Task | None:
    return _tasks.pop(task_id, None)
