from datetime import date

from fastapi.testclient import TestClient

from app.main import app
from app import store


client = TestClient(app)


def setup_function() -> None:
    store.clear_entries()


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_entry_creates_and_returns_entry() -> None:
    payload = {
        "date": "2026-04-15",
        "person": "Ato Toffah",
        "team": "Backend",
        "description": "Write FastAPI endpoints",
        "duration_minutes": 60,
    }
    response = client.post("/api/entries", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] >= 1
    assert body["person"] == "Ato Toffah"


def test_get_entries_lists_seed_plus_new() -> None:
    # Seed has 3 entries
    response = client.get("/api/entries")
    assert response.status_code == 200
    initial_count = len(response.json())

    payload = {
        "date": "2026-04-15",
        "person": "Ato Toffah",
        "team": "Backend",
        "description": "Write FastAPI endpoints",
        "duration_minutes": 60,
    }
    client.post("/api/entries", json=payload)

    response = client.get("/api/entries")
    assert response.status_code == 200
    assert len(response.json()) == initial_count + 1


def test_get_entries_filters_by_date() -> None:
    response = client.get("/api/entries", params={"date": "2026-04-13"})
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 2
    assert all(item["date"] == "2026-04-13" for item in items)


def test_get_entries_filters_by_person_case_insensitive() -> None:
    response = client.get("/api/entries", params={"person": "sara gordic"})
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 2
    assert all(item["person"] == "Sara Gordic" for item in items)


def test_validation_rejects_empty_person() -> None:
    payload = {
        "date": "2026-04-15",
        "person": " ",
        "team": "Backend",
        "description": "Write FastAPI endpoints",
        "duration_minutes": 60,
    }
    response = client.post("/api/entries", json=payload)
    assert response.status_code == 422
