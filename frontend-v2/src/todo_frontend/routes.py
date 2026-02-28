from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from . import client

router = APIRouter()
templates: Jinja2Templates | None = None


def set_templates(t: Jinja2Templates) -> None:
    global templates
    templates = t


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    error = None
    tasks = []
    try:
        tasks = await client.get_tasks()
    except Exception as e:
        error = f"Could not load tasks: {e}"
    return templates.TemplateResponse(
        "index.html", {"request": request, "tasks": tasks, "error": error}
    )


@router.post("/tasks")
async def create_task(
    title: str = Form(...),
    description: str = Form(""),
):
    await client.create_task(title, description)
    return RedirectResponse("/", status_code=303)


@router.post("/tasks/{task_id}/status")
async def update_status(task_id: str, status: str = Form(...)):
    await client.update_task_status(task_id, status)
    return RedirectResponse("/", status_code=303)


@router.post("/tasks/{task_id}/delete")
async def delete_task(task_id: str):
    await client.delete_task(task_id)
    return RedirectResponse("/", status_code=303)


@router.get("/tasks/{task_id}/history", response_class=HTMLResponse)
async def task_history(request: Request, task_id: str):
    error = None
    events = []
    try:
        events = await client.get_history(task_id)
    except Exception as e:
        error = f"Could not load history: {e}"
    return templates.TemplateResponse(
        "history.html",
        {"request": request, "task_id": task_id, "events": events, "error": error},
    )
