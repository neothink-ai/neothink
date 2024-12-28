
from fastapi import APIRouter, HTTPException
from database import Database
from bson.json_util import dumps

router = APIRouter(
    prefix="/teams",
    tags=["teams"]
)

db = Database.get_db()

@router.get("/user/{user_id}")
async def fetch_teams(user_id: str):
    try:
        teams_collection = db["Teams"]["teams"]
        data = teams_collection.find({"users": user_id})
        return dumps(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add/{team_id}/{user_id}")
async def add_user_to_team(team_id: str, user_id: str):
    try:
        teams_collection = db["Teams"]["teams"]
        result = teams_collection.update_one(
            {"team_id": team_id},
            {"$addToSet": {"users": user_id}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Team not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def fetch_all_teams():
    try:
        teams_collection = db["Teams"]["teams"]
        data = teams_collection.find()
        return dumps(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))