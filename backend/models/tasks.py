from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    title: str = Field(..., min_length=1)
    columnId: str = Field(..., min_length=1)
    userid: str = Field(..., min_length=1)
    state: str = Field(None)
    priority: str = Field(default="Medium")
    size: str = Field(default="Medium")
    description: str = Field(default="")
    deadline: Optional[str] = None
    assignee: Optional[str] = None
    assigned_time: Optional[str] = None
    completed_time: Optional[str] = None

    @validator('state', pre=True, always=True)
    def set_state(cls, v, values):
        return v or values.get('columnId', 'todo')

    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Example Task",
                "columnId": "todo",
                "userid": "user123",
                "state": "todo",
                "priority": "Medium",
                "size": "Medium",
                "description": "",
                "deadline": None,
                "assignee": None,
                "assigned_time": None,
                "completed_time": None
            }
        }
    }