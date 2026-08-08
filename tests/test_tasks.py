from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Docker",
            "description": "Complete Docker labs",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] >= 1
    assert data["title"] == "Learn Docker"
    assert data["description"] == "Complete Docker labs"
    assert data["completed"] is False


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Kubernetes",
            "description": "Complete Kubernetes labs",
        },
    )

    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Learn Kubernetes"


def test_get_nonexistent_task():
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task():
    # Create a task
    response = client.post(
        "/tasks",
        json={
            "title": "Task to Delete",
            "description": "This task will be deleted",
        },
    )

    assert response.status_code == 200

    task_id = response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully"}

    # Verify the task no longer exists
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
