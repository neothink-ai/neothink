from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional, List
import requests
import json
from pymongo import MongoClient
from bson.json_util import dumps
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# MongoDB setup
client = MongoClient("mongodb+srv://neothink_deploy:neothinkisthebest@neothink.xnzwv.mongodb.net/?retryWrites=true&w=majority&appName=neothink")


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
        users_db = client["Users"]
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
        users_db = client["Users"]
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
        teams_db = client["Teams"]
        teams_collection = teams_db["teams"]
        data = teams_collection.find({"users": user_id})
        json_data = dumps(data)
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/add-user-to-team/{team_id}/{user_id}")
async def add_user_to_team(team_id: str, user_id: str):
    try:
        teams_db = client["Teams"]
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
        teams_db = client["Teams"]
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
        teams_db = client["Teams"]
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
        users_db = client["Users"]
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
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6876)