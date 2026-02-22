# Frontend

Static HTML/CSS/JS todo app. No frameworks, no build step.

## Development
```bash
python3 -m http.server 3000 --directory .
# Open http://localhost:3000
```

## Configuration
- `API_BASE = 'http://localhost:8000'` — todo-api
- `PROGRESS_BASE = 'http://localhost:8001'` — todo-progress-api

## Features
- Create, start, complete, delete tasks
- View progress history in a modal
- All API calls use async/await with try/catch
