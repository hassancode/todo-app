# =============================================================================
# Stage 1: Builder — install dependencies and build the project
# =============================================================================
FROM ghcr.io/astral-sh/uv:python3.9-bookworm-slim AS builder

WORKDIR /app

# Compile .pyc files at build time; use copy instead of symlinks for portability
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies only (no project source) — cached unless lock file changes
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

# Copy source and install the project into the virtualenv
COPY src/ src/
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# =============================================================================
# Stage 2: Runtime — lean image with no build tooling
# =============================================================================
FROM python:3.9-slim-bookworm AS runtime

# Non-root user for security
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

WORKDIR /app

# Copy only the virtualenv and source from the builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src  /app/src

USER app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "todo_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
