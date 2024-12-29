from fastapi import APIRouter, HTTPException, Query
from models.tasks import Task
from database import Database
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
from typing import Optional
from datetime import datetime

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

db = Database.get_db()

@router.get("")
async def get_tasks(userid: Optional[str] = None):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        query = {"userid": userid} if userid else {}
        cursor = tasks_collection.find(query)
        tasks_list = list(cursor)
        if not tasks_list and userid:
            return []  # Return empty list instead of 404 for no tasks
        serialized_tasks = json.loads(dumps(tasks_list))
        return serialized_tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
async def create_task(task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        
        task_dict = task.model_dump(exclude_none=True)
        # Ensure required timestamps
        now = datetime.utcnow().isoformat()
        task_dict.update({
            "created_time": now,
            "assigned_time": task_dict.get("assigned_time") or now,
        })
        
        result = tasks_collection.insert_one(task_dict)
        
        return {
            "_id": {"$oid": str(result.inserted_id)},
            **task_dict
        }
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
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
