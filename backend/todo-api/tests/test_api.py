from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from todo_api.main import app
from todo_api import storage


@pytest.fixture(autouse=True)
def clear_storage():
    storage._tasks.clear()
    yield
    storage._tasks.clear()


@pytest.fixture(autouse=True)
def mock_record_event():
    with patch("todo_api.routes.record_event", new_callable=AsyncMock):
        yield


@pytest.fixture
def client():
    return TestClient(app)


# --- Health ---

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# --- Create ---

def test_create_task(client):
    resp = client.post("/tasks/", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["description"] == ""
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_with_description(client):
    resp = client.post("/tasks/", json={"title": "Buy milk", "description": "2% fat"})
    assert resp.status_code == 201
    assert resp.json()["description"] == "2% fat"


def test_create_task_missing_title(client):
    resp = client.post("/tasks/", json={})
    assert resp.status_code == 422


# --- List ---

def test_list_tasks_empty(client):
    resp = client.get("/tasks/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_tasks(client):
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})
    resp = client.get("/tasks/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


# --- Get ---

def test_get_task(client):
    created = client.post("/tasks/", json={"title": "Buy milk"}).json()
    resp = client.get(f"/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_task_not_found(client):
    resp = client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


# --- Update ---

def test_update_task_status(client):
    created = client.post("/tasks/", json={"title": "Buy milk"}).json()
    resp = client.put(f"/tasks/{created['id']}", json={"status": "in_progress"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"


def test_update_task_title(client):
    created = client.post("/tasks/", json={"title": "Buy milk"}).json()
    resp = client.put(f"/tasks/{created['id']}", json={"title": "Buy oat milk"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Buy oat milk"


def test_update_task_not_found(client):
    resp = client.put("/tasks/00000000-0000-0000-0000-000000000000", json={"title": "x"})
    assert resp.status_code == 404


def test_update_task_invalid_status(client):
    created = client.post("/tasks/", json={"title": "Buy milk"}).json()
    resp = client.put(f"/tasks/{created['id']}", json={"status": "unknown"})
    assert resp.status_code == 422


# --- Delete ---

def test_delete_task(client):
    created = client.post("/tasks/", json={"title": "Buy milk"}).json()
    resp = client.delete(f"/tasks/{created['id']}")
    assert resp.status_code == 204
    # Verify it's gone
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found(client):
    resp = client.delete("/tasks/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404


def test_delete_removes_from_list(client):
    created = client.post("/tasks/", json={"title": "Buy milk"}).json()
    client.delete(f"/tasks/{created['id']}")
    tasks = client.get("/tasks/").json()
    assert all(t["id"] != created["id"] for t in tasks)
