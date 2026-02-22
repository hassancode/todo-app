from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from todo_progress_api.main import app
from todo_progress_api import storage


@pytest.fixture(autouse=True)
def clear_storage():
    storage._events.clear()
    yield
    storage._events.clear()


@pytest.fixture
def client():
    return TestClient(app)


# --- Health ---

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# --- Record event ---

def test_record_event(client):
    task_id = str(uuid.uuid4())
    resp = client.post("/progress/", json={
        "task_id": task_id,
        "event_type": "created",
        "old_status": None,
        "new_status": "pending",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["task_id"] == task_id
    assert data["event_type"] == "created"
    assert data["old_status"] is None
    assert data["new_status"] == "pending"
    assert "id" in data
    assert "timestamp" in data


def test_record_event_updated(client):
    task_id = str(uuid.uuid4())
    resp = client.post("/progress/", json={
        "task_id": task_id,
        "event_type": "updated",
        "old_status": "pending",
        "new_status": "in_progress",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["old_status"] == "pending"
    assert data["new_status"] == "in_progress"


def test_record_event_deleted(client):
    task_id = str(uuid.uuid4())
    resp = client.post("/progress/", json={
        "task_id": task_id,
        "event_type": "deleted",
        "old_status": "in_progress",
        "new_status": None,
    })
    assert resp.status_code == 201
    assert resp.json()["new_status"] is None


def test_record_event_invalid_type(client):
    resp = client.post("/progress/", json={
        "task_id": str(uuid.uuid4()),
        "event_type": "unknown",
    })
    assert resp.status_code == 422


def test_record_event_missing_task_id(client):
    resp = client.post("/progress/", json={"event_type": "created"})
    assert resp.status_code == 422


# --- List events ---

def test_list_events_empty(client):
    resp = client.get("/progress/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_events(client):
    task_id = str(uuid.uuid4())
    client.post("/progress/", json={"task_id": task_id, "event_type": "created", "new_status": "pending"})
    client.post("/progress/", json={"task_id": task_id, "event_type": "updated", "old_status": "pending", "new_status": "in_progress"})
    resp = client.get("/progress/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


# --- Get events for task ---

def test_get_events_for_task(client):
    task_id_1 = str(uuid.uuid4())
    task_id_2 = str(uuid.uuid4())
    client.post("/progress/", json={"task_id": task_id_1, "event_type": "created", "new_status": "pending"})
    client.post("/progress/", json={"task_id": task_id_2, "event_type": "created", "new_status": "pending"})
    resp = client.get(f"/progress/{task_id_1}")
    assert resp.status_code == 200
    events = resp.json()
    assert len(events) == 1
    assert events[0]["task_id"] == task_id_1


def test_get_events_for_task_multiple_events(client):
    task_id = str(uuid.uuid4())
    client.post("/progress/", json={"task_id": task_id, "event_type": "created", "new_status": "pending"})
    client.post("/progress/", json={"task_id": task_id, "event_type": "updated", "old_status": "pending", "new_status": "in_progress"})
    resp = client.get(f"/progress/{task_id}")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_events_for_unknown_task(client):
    resp = client.get(f"/progress/{uuid.uuid4()}")
    assert resp.status_code == 200
    assert resp.json() == []
