# Todo Progress API

FastAPI service that records task lifecycle events from todo-api.

## Run
```bash
uv run uvicorn todo_progress_api.main:app --host 0.0.0.0 --port 8001 --reload
```

## Endpoints
- POST /progress           — record an event
- GET  /progress           — list all events
- GET  /progress/{task_id} — get events for a specific task
- GET  /health             — health check

## Docs
http://localhost:8001/docs
