
from fastapi import APIRouter, HTTPException
from models import UserProfileUpdate
from database import Database
from bson.json_util import dumps

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

db = Database.get_db()

@router.get("/profile/{user_id}")
async def fetch_user(user_id: str):
    try:
        user_data_collection = db["Users"]["user_data"]
        data = user_data_collection.find_one({"user_id": user_id})
        if data:
            return dumps(data)
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile/{user_id}")
async def update_profile(user_id: str, profile: UserProfileUpdate):
    try:
        user_data_collection = db["Users"]["user_data"]
        result = user_data_collection.update_one(
            {"user_id": user_id},
            {"$set": profile.model_dump()},
            upsert=True
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))