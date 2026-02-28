from __future__ import annotations

import httpx

TODO_API = "http://localhost:8000"
PROGRESS_API = "http://localhost:8001"
TIMEOUT = 5.0


async def get_tasks() -> list[dict]:
    async with httpx.AsyncClient(base_url=TODO_API, timeout=TIMEOUT) as client:
        r = await client.get("/tasks")
        r.raise_for_status()
        return r.json()


async def create_task(title: str, description: str) -> dict:
    async with httpx.AsyncClient(base_url=TODO_API, timeout=TIMEOUT) as client:
        r = await client.post("/tasks", json={"title": title, "description": description})
        r.raise_for_status()
        return r.json()


async def update_task_status(task_id: str, status: str) -> dict:
    async with httpx.AsyncClient(base_url=TODO_API, timeout=TIMEOUT) as client:
        r = await client.put(f"/tasks/{task_id}", json={"status": status})
        r.raise_for_status()
        return r.json()


async def delete_task(task_id: str) -> None:
    async with httpx.AsyncClient(base_url=TODO_API, timeout=TIMEOUT) as client:
        r = await client.delete(f"/tasks/{task_id}")
        r.raise_for_status()


async def get_history(task_id: str) -> list[dict]:
    async with httpx.AsyncClient(base_url=PROGRESS_API, timeout=TIMEOUT) as client:
        r = await client.get(f"/progress/{task_id}")
        r.raise_for_status()
        return r.json()
