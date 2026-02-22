# Todo App Monorepo

A local-dev todo application consisting of three components:

## Architecture

```
Browser (frontend/)
    │  HTTP fetch calls
    ▼
todo-api (port 8000)          ← CRUD for tasks
    │  fire-and-forget POST
    ▼
todo-progress-api (port 8001) ← records lifecycle events
```

All storage is in-memory. No database required.

## Components

| Component | Directory | Port | Description |
|-----------|-----------|------|-------------|
| Frontend | `frontend/` | 3000 | Static HTML/CSS/JS, no build step |
| Todo API | `backend/todo-api/` | 8000 | FastAPI CRUD for tasks |
| Progress API | `backend/todo-progress-api/` | 8001 | FastAPI event tracker |

## Startup Order

**Start services in this order** (progress-api must be up before todo-api starts making requests to it):

### Terminal 1 — Progress API
```bash
cd backend/todo-progress-api
uv run uvicorn todo_progress_api.main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 2 — Todo API
```bash
cd backend/todo-api
uv run uvicorn todo_api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 3 — Frontend
```bash
python3 -m http.server 3000 --directory frontend/
```

Then open http://localhost:3000 in your browser.

## API Documentation (Swagger UI)

- Todo API: http://localhost:8000/docs
- Progress API: http://localhost:8001/docs

## Health Checks

```bash
curl http://localhost:8000/health   # {"status":"ok"}
curl http://localhost:8001/health   # {"status":"ok"}
```
