from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routes import router, set_templates

BASE_DIR = Path(__file__).resolve().parents[2]  # frontend-v2/

app = FastAPI(title="Todo Frontend v2", redirect_slashes=False)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
set_templates(templates)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(router)


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})
