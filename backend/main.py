from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
import requests
import json
from database import Database
from bson.json_util import dumps
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remove the direct client connection and use Database class instead
db = Database.get_db()

# Pydantic model for incoming JSON data
class Item(BaseModel):
    key: str
    value: Any

class UserProfileUpdate(BaseModel):
    _id: Item
    user_id: str
    first_name: Optional[str]
    last_name: Optional[str]
    department: Optional[str]
    skills: Optional[List[str]]
    teams: Optional[List[str]]

# Task model
class Task(BaseModel):
    title: str
    columnId: str
    state: str  # Add state field
    priority: str = Field(default="Medium")
    deadline: Optional[str] = None  # Change from datetime to str
    size: str = Field(default="Medium")
    assignee: Optional[str] = None
    assigned_time: Optional[str] = None  # Change from datetime to str
    completed_time: Optional[str] = None  # Change from datetime to str

@app.post("/process-json")
async def process_json(item: Item):
    prompt = "JSON responses only. Do not include any syntax highlighting or any other english sentences above or below the json you will output. Use the key 'this' to say 'Hello World'"

    data = {
        "prompt": prompt,
        "model": 'llama3.1',
        "format": "json",
        "stream": False,
        "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100},
    }

    response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)
    json_data = json.loads(response.text)

    # print(json.dumps(json.loads(json_data["response"]), indent=2))

    return response

@app.get("/fetch-mongodb")
async def fetch_mongodb():
    try:
        users_db = db["Users"]
        collection = users_db["user_data"]
        data = collection.find()
        json_data = dumps(data)
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fetch-user/{user_id}")
async def fetch_user(user_id: str):
    # print(f"Received fetch-user request: {user_id}")
    try:
        users_db = db["Users"]
        user_data_collection = users_db["user_data"]
        data = user_data_collection.find_one({"user_id": user_id})
        if data:
            json_data = dumps(data)
            return json_data
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fetch-teams/{user_id}")
async def fetch_teams(user_id: str):
    # print(f"Received fetch-teams request: {user_id}")
    try:
        teams_db = db["Teams"]
        teams_collection = teams_db["teams"]
        data = teams_collection.find({"users": user_id})
        json_data = dumps(data)
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/add-user-to-team/{team_id}/{user_id}")
async def add_user_to_team(team_id: str, user_id: str):
    try:
        teams_db = db["Teams"]
        teams_collection = teams_db["teams"]
        result = teams_collection.update_one(
            {"team_id": team_id},
            {"$addToSet": {"users": user_id}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/remove-user-from-team/{team_id}/{user_id}")
async def remove_user_from_team(team_id: str, user_id: str):
    try:
        teams_db = db["Teams"]
        teams_collection = teams_db["teams"]
        result = teams_collection.update_one(
            {"team_id": team_id},
            {"$pull": {"users": user_id}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fetch-all-teams")
async def fetch_all_teams():
    try:
        teams_db = db["Teams"]
        teams_collection = teams_db["teams"]
        data = teams_collection.find()
        json_data = dumps(data)
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/update-profile/{user_id}")
async def update_profile(user_id: str, profile: UserProfileUpdate):
    # print(f"Received update-profile request: {user_id}")
    # print("Profile data:")
    # print(profile.model_dump_json())
    # print(type(profile.model_dump()))
    try:
        users_db = db["Users"]
        user_data_collection = users_db["user_data"]
        # print("Collection fetched. Performing update")
        result = user_data_collection.update_one(
            {"user_id": user_id},
            {"$set": profile.model_dump()},
            upsert=True
        )
        # print("Supposedly updated")
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success"}
    except Exception as e:
        # print("Encountered error: ")
        # print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
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

@app.post("/tasks")
async def create_task(task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        task_dict = task.model_dump()
        task_dict["assigned_time"] = datetime.now().isoformat()  # Convert to ISO string
        if task_dict["state"] == "done":
            task_dict["completed_time"] = datetime.now().isoformat()  # Convert to ISO string
        print(f"Creating task: {task_dict}")  # Debug log
        result = tasks_collection.insert_one(task_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error creating task: {e}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    try:
        tasks_collection = db["Tasks"]["tasks"]
        task_dict = task.model_dump()
        if task_dict["state"] == "done":
            task_dict["completed_time"] = datetime.now()
        from bson.objectid import ObjectId
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": task_dict}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        tasks_db = db["Tasks"]
        tasks_collection = tasks_db["tasks"]
        from bson.objectid import ObjectId
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.on_event("shutdown")
async def shutdown_event():
    Database.close_connection()
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6876)