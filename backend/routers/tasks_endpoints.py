from fastapi import APIRouter, HTTPException
from typing import List
from models.tasks import Task
from utils.tasks_utils import create_task, get_tasks_by_user, update_task, delete_task

router = APIRouter()

@router.post("/tasks", response_model=str)
def create_new_task(task: Task):
    task_data = task.dict(exclude_unset=True)
    task_id = create_task(task_data)
    return str(task_id)

@router.get("/tasks", response_model=List[Task])
def get_user_tasks(userid: str):
    tasks = get_tasks_by_user(userid)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

@router.put("/tasks/{task_id}")
def update_existing_task(task_id: str, task: Task):
    result = update_task(task_id, task.dict(exclude_unset=True))
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated successfully"}

@router.delete("/tasks/{task_id}")
def delete_existing_task(task_id: str):
    result = delete_task(task_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}