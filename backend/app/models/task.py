from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    id: Optional[str]  # MongoDB ObjectId, optional for creation
    userid: str  # Logged-in user's ID from Firebase
    title: str  # Add title field
    columnId: str  # Changed from columnID to match frontend
    assignee: Optional[str]  # Assignee's ID (optional initially)
    deadline: Optional[datetime]  # Deadline for the task
    description: Optional[str]  # Add description field
    priority: str  # Task priority (e.g., "low", "medium", "high")
    size: str  # Task size (e.g., "small", "medium", "large")
    created_time: datetime = Field(default_factory=datetime.utcnow)  # Automatically set to now
    assigned_time: Optional[datetime]  # Set when task is assigned
    completed_time: Optional[datetime]  # Set when task is completed
    
    class Config:
        allow_population_by_field_name = True
