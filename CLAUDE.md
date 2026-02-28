# Todo App Monorepo

A local-dev todo application with two frontend options backed by the same APIs:

## Architecture

```
Browser (frontend/ or frontend-v2/)
    │  HTTP fetch calls (frontend) or server-side httpx (frontend-v2)
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
| Frontend (static) | `frontend/` | 3000 | Static HTML/CSS/JS, no build step |
| Frontend v2 (SSR) | `frontend-v2/` | 3001 | FastAPI + Jinja2, server-side rendered, no client JS |
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

### Terminal 3 — Frontend (static)
```bash
python3 -m http.server 3000 --directory frontend/
```

### Terminal 3 (alternative) — Frontend v2 (SSR)
```bash
cd frontend-v2
uv run uvicorn todo_frontend.main:app --host 0.0.0.0 --port 3001 --reload
```

Then open http://localhost:3000 (static) or http://localhost:3001 (SSR) in your browser.

## Docker

Each service has its own `Dockerfile` and `.dockerignore`. All images are security-hardened:
- Python services run as non-root `appuser` (UID 1001) on Python 3.13
- Base images are digest-pinned for reproducible, tamper-proof builds
- No dev dependencies included in images

### Build Images

```bash
# Build all images (first time or after code changes)
docker build -t todo-frontend:latest ./frontend/
docker build -t todo-frontend-v2:latest ./frontend-v2/
docker build -t todo-api:latest ./backend/todo-api/
docker build -t todo-progress-api:latest ./backend/todo-progress-api/
```

### Docker Compose

```bash
# Start all services (detached)
docker compose up -d

# Stop and remove all services
docker compose down
```

`--workers 1` is required for in-memory storage (baked into the Dockerfiles).
The `PROGRESS_API_URL` env var wires todo-api to todo-progress-api by service name.

### Individual Containers

Services require a shared Docker network to resolve each other by hostname:

```bash
docker network create todo-net

docker run -d --name todo-progress-api --network todo-net -p 8001:8001 todo-progress-api:latest
docker run -d --name todo-api          --network todo-net -p 8000:8000 todo-api:latest
docker run -d --name todo-frontend-v2  --network todo-net -p 3001:3001 todo-frontend-v2:latest
docker run -d --name todo-frontend     --network todo-net -p 3000:80   todo-frontend:latest
```

## API Documentation (Swagger UI)

- Todo API: http://localhost:8000/docs
- Progress API: http://localhost:8001/docs

## Health Checks

```bash
curl http://localhost:8000/health   # {"status":"ok"}
curl http://localhost:8001/health   # {"status":"ok"}
curl http://localhost:3000/health   # {"status":"ok"}
curl http://localhost:3001/health   # {"status":"ok"}
```
