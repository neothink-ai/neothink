from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from models.tasks import Task
from database import Database
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import json
from typing import Optional
from datetime import datetime

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

db = Database.get_db()

@router.options("")
async def options_handler():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, DELETE, PUT, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )

@router.get("")
async def get_tasks(userid: Optional[str] = None):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        query = {"userid": userid} if userid else {}
        cursor = tasks_collection.find(query)
        tasks_list = list(cursor)
        
        # Convert tasks to JSON-serializable format
        serialized_tasks = json.loads(dumps(tasks_list))
        
        # Log for debugging
        print(f"Fetched tasks for user {userid}:", serialized_tasks)
        
        return serialized_tasks
    except Exception as e:
        print(f"Error fetching tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
async def create_task(task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        
        # Convert the task to a dict and remove None values
        task_dict = {k: v for k, v in task.model_dump().items() if v is not None}
        
        # Insert the task
        result = tasks_collection.insert_one(task_dict)
        
        # Create response data
        response_data = task_dict.copy()
        response_data["_id"] = str(result.inserted_id)
        
        # Return a JSONResponse directly
        return JSONResponse(content=response_data)
        
    except Exception as e:
        print(f"Error creating task: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=422,
            detail=f"Error creating task: {str(e)}"
        )

@router.put("/{task_id}")
async def update_task(task_id: str, task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        obj_id = ObjectId(task_id)
        update_data = {
            "userid": task.userid,
            "assignee": task.assignee,
            "deadline": task.deadline,
            "assigned_time": task.assigned_time,
            "completed_time": task.completed_time,
            "size": task.size,
            "priority": task.priority,
            "columnID": task.columnID
        }
        result = tasks_collection.update_one(
            {"_id": obj_id}, 
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success", "columnID": task.columnID}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
