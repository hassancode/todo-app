# Todo API

FastAPI CRUD service for tasks. Notifies todo-progress-api of lifecycle events.

## Run
```bash
uv run uvicorn todo_api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints
- POST   /tasks       — create task
- GET    /tasks       — list all tasks
- GET    /tasks/{id}  — get task
- PUT    /tasks/{id}  — update task
- DELETE /tasks/{id}  — delete task
- GET    /health      — health check

## Docs
http://localhost:8000/docs
