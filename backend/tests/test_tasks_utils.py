import pytest
from bson.objectid import ObjectId
from utils.tasks_utils import create_task, get_tasks_by_user, update_task, delete_task
from database import Database

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

def test_create_task(db, task_data):
    task_id = create_task(task_data)
    assert isinstance(task_id, ObjectId)

def test_get_tasks_by_user(db, task_data):
    tasks = get_tasks_by_user(task_data["userid"])
    assert isinstance(tasks, list)

def test_update_task(db, task_data):
    task_id = create_task(task_data)
    updated_data = {"priority": "High"}
    result = update_task(task_id, updated_data)
    assert result.matched_count == 1

def test_delete_task(db, task_data):
    task_id = create_task(task_data)
    result = delete_task(task_id)
    assert result.deleted_count == 1
