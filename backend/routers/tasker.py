from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from database import Database
from openai import generate_tasks_from_description

class TaskRequest(BaseModel):
    project_description: str
    userid: str

router = APIRouter()
db = Database.get_db()

@router.post("/generate-tasks")  # Remove trailing slash
async def generate_tasks(request: TaskRequest):  # Change to use request body
    try:
        print(f"Processing request: {request}")
        tasks = await generate_tasks_from_description(request.project_description)
        
        tasks_collection = db["Tasks"]["temp_tasks"]
        task_objects = []
        
        for task in tasks:
            task['userid'] = request.userid
            result = tasks_collection.insert_one(task)
            task['_id'] = str(result.inserted_id)
            task_objects.append(task)
        
        return {"status": "success", "tasks": task_objects}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
