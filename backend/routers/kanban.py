from fastapi import APIRouter, HTTPException
from models import Task
from database import Database
from bson.objectid import ObjectId
from bson.json_util import dumps
import json

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

db = Database.get_db()

@router.get("")
async def get_tasks():
    try:
        tasks_collection = db["Tasks"]["tasks"]
        cursor = tasks_collection.find()
        tasks_list = list(cursor)
        serialized_tasks = json.loads(dumps(tasks_list))
        return serialized_tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
async def create_task(task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        task_dict = {
            "title": task.title,
            "columnId": task.columnId
        }
        result = tasks_collection.insert_one(task_dict)
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{task_id}")
async def update_task(task_id: str, task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        obj_id = ObjectId(task_id)
        update_data = {
            "title": task.title,
            "columnId": task.columnId
        }
        result = tasks_collection.update_one(
            {"_id": obj_id}, 
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success", "columnId": task.columnId}
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
