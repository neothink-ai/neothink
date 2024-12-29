from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    title: str = Field(..., min_length=1, description="Task title")
    columnId: str = Field(..., min_length=1, description="Column identifier")
    userid: str = Field(..., min_length=1, description="User identifier")
    state: Optional[str] = None
    priority: str = Field(default="Medium")
    size: str = Field(default="Medium")
    description: str = Field(default="")
    deadline: Optional[str] = None
    assignee: Optional[str] = None
    assigned_time: Optional[str] = None
    completed_time: Optional[str] = None
    created_time: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def set_defaults(cls, values):
        if isinstance(values, dict):
            values['state'] = values.get('state') or values.get('columnId', 'todo')
            values['description'] = values.get('description', '')
            values['priority'] = values.get('priority', 'Medium')
            values['size'] = values.get('size', 'Medium')
            # Convert empty strings to None
            for key in values:
                if values[key] == "":
                    values[key] = None
        return values

    model_config = {
        "json_schema_extra": {
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
                "completed_time": None,
                "created_time": None
            }
        }
    }