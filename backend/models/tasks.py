from pydantic import BaseModel, Field, model_validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Task(BaseModel):
    title: str
    columnId: str
    userid: str
    state: str
    priority: str = "Medium"
    size: str = "Medium"
    description: Optional[str] = ""
    deadline: Optional[str] = None
    assignee: Optional[str] = None
    assigned_time: Optional[str] = None
    completed_time: Optional[str] = None
    created_time: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def handle_objectid(cls, values):
        if isinstance(values, dict):
            # Handle _id field if present
            if '_id' in values:
                if isinstance(values['_id'], dict) and '$oid' in values['_id']:
                    values['_id'] = values['_id']['$oid']
                elif isinstance(values['_id'], ObjectId):
                    values['_id'] = str(values['_id'])
        return values

    class Config:
        from_attributes = True
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string when serializing
        }