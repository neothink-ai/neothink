
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    id: Optional[str]  # MongoDB ObjectId, optional for creation
    userid: str        # Firebase user ID
    assignee: Optional[str]
    deadline: Optional[datetime]
    created_time: datetime = Field(default_factory=datetime.utcnow)
    assigned_time: Optional[datetime]
    completed_time: Optional[datetime]
    size: str
    priority: str
    columnID: str      # e.g. "todo", "inprogress", "done"