
from fastapi import APIRouter, HTTPException
from typing import List
from bson.objectid import ObjectId
from bson.json_util import dumps
import json

from database import Database
from models.tasks import Task

router = APIRouter()
db = Database.get_db()

@router.get("/tasks")
async def get_tasks():
    try:
        tasks_collection = db["Tasks"]["tasks"]
        cursor = tasks_collection.find()
        tasks_list = list(cursor)
        print("MongoDB connection:", db)  # Debug log
        print("Collection:", tasks_collection)  # Debug log
        print("Raw tasks from MongoDB:", tasks_list)  # Debug log
        
        # Convert MongoDB cursor to list and then to JSON
        serialized_tasks = json.loads(dumps(tasks_list))
        print("Serialized tasks:", serialized_tasks)  # Debug log
        
        return serialized_tasks
    except Exception as e:
        print(f"Error in get_tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks")
async def create_task(task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        task_dict = {
            "userid": task.userid,
            "assignee": task.assignee,
            "deadline": task.deadline,
            "created_time": task.created_time,
            "assigned_time": task.assigned_time,
            "completed_time": task.completed_time,
            "size": task.size,
            "priority": task.priority,
            "columnID": task.columnID
        }
        result = tasks_collection.insert_one(task_dict)
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tasks/{task_id}")
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
        result = tasks_collection.update_one({"_id": obj_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        tasks_db = db["Tasks"]
        tasks_collection = tasks_db["tasks"]
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))