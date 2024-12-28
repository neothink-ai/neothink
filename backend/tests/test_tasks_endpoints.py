import pytest
from fastapi.testclient import TestClient
from main import app
from database import Database

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = Database.get_db()
    yield db
    Database.close_connection()

@pytest.fixture
def task_data():
    return {
        "userid": "test_user",
        "assignee": "test_assignee",
        "deadline": None,
        "created_time": "2023-01-01T00:00:00Z",
        "assigned_time": None,
        "completed_time": None,
        "size": "Medium",
        "priority": "Medium",
        "columnID": "todo"
    }

def test_create_task_endpoint(db, task_data):
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    assert "inserted_id" in response.json()

def test_get_tasks_endpoint(db, task_data):
    response = client.get("/tasks", params={"userid": task_data["userid"]})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task_endpoint(db, task_data):
    task_id = client.post("/tasks", json=task_data).json()["inserted_id"]
    updated_data = {"priority": "High"}
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_delete_task_endpoint(db, task_data):
    task_id = client.post("/tasks", json=task_data).json()["inserted_id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
