"""API tests using FastAPI's TestClient."""

import pytest


def test_get_todos_starts_empty(client):
    response = client.get("/todos")

    assert response.status_code == 200
    assert response.json() == []


def test_post_todo_returns_created_item(client):
    response = client.post("/todos", json={"title": "Buy milk"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Buy milk", "done": False, "due_date": None}

    listed = client.get("/todos")
    assert listed.json() == [{"id": 1, "title": "Buy milk", "done": False, "due_date": None}]


def test_post_todo_rejects_blank_title(client):
    response = client.post("/todos", json={"title": ""})

    assert response.status_code == 422
    assert client.get("/todos").json() == []


def test_post_todo_with_valid_due_date(client):
    response = client.post("/todos", json={"title": "Pay rent", "due_date": "2026-12-01"})

    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-12-01"
    assert client.get("/todos").json()[0]["due_date"] == "2026-12-01"


def test_post_todo_without_due_date_has_null_due_date(client):
    response = client.post("/todos", json={"title": "Someday"})

    assert response.status_code == 201
    assert response.json()["due_date"] is None


def test_post_todo_accepts_explicit_null_due_date(client):
    response = client.post("/todos", json={"title": "Someday", "due_date": None})

    assert response.status_code == 201
    assert response.json()["due_date"] is None


@pytest.mark.parametrize("bad_date", ["2026-13-45", "not-a-date", "2026-02-30"])
def test_post_todo_rejects_invalid_due_date(client, bad_date):
    response = client.post("/todos", json={"title": "Bad", "due_date": bad_date})

    assert response.status_code == 422
    assert client.get("/todos").json() == []


def test_patch_toggles_done(client):
    created = client.post("/todos", json={"title": "Walk dog"}).json()

    toggled = client.patch(f"/todos/{created['id']}")
    assert toggled.status_code == 200
    assert toggled.json()["done"] is True

    toggled_back = client.patch(f"/todos/{created['id']}")
    assert toggled_back.status_code == 200
    assert toggled_back.json()["done"] is False


def test_patch_missing_todo_returns_404(client):
    response = client.patch("/todos/42")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_delete_todo(client):
    created = client.post("/todos", json={"title": "Temporary"}).json()

    response = client.delete(f"/todos/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/todos").json() == []


def test_delete_missing_todo_returns_404(client):
    response = client.delete("/todos/42")

    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_index_serves_todo_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    body = response.text
    assert "<h1>Todo</h1>" in body
    assert 'id="add-form"' in body
    assert 'method: "PATCH"' in body
    assert 'method: "DELETE"' in body
    assert 'method: "POST"' in body
    assert "todo.due_date" in body
