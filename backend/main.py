from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict
import requests
import json
from pymongo import MongoClient
from bson.json_util import dumps

app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb+srv://neothinkai:<db_password>@cluster0.xnzwv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


# Pydantic model for incoming JSON data
class Item(BaseModel):
    key: str
    value: Any

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

    print(json.dumps(json.loads(json_data["response"]), indent=2))

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
    try:
        teams_db = client["Teams"]
        teams_collection = teams_db["teams"]
        data = teams_collection.find({"users": user_id})
        json_data = dumps(data)
        return json_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=6876)