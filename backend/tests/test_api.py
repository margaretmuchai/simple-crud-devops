import pytest


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running 🚀"}


def test_get_empty_tasks(client):
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data


def test_get_all_tasks(client):
    client.post("/api/tasks", json={"title": "Task 1", "description": "Desc 1"})
    client.post("/api/tasks", json={"title": "Task 2", "description": "Desc 2"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_single_task(client):
    create_response = client.post(
        "/api/tasks",
        json={"title": "Single Task", "description": "Single Desc"}
    )
    task_id = create_response.json()["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Single Task"
    assert data["description"] == "Single Desc"


def test_get_single_task_not_found(client):
    response = client.get("/api/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task(client):
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original", "description": "Original Desc"}
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "description": "Updated Desc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["description"] == "Updated Desc"


def test_update_task_not_found(client):
    response = client.put(
        "/api/tasks/999",
        json={"title": "Updated", "description": "Updated Desc"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task(client):
    create_response = client.post(
        "/api/tasks",
        json={"title": "To Delete", "description": "Will be deleted"}
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}

    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_create_task_validation_error(client):
    response = client.post("/api/tasks", json={})
    assert response.status_code == 422