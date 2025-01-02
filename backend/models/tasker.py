from pydantic import BaseModel
from typing import List, Optional

class TaskGenerationRequest(BaseModel):
    project_description: str
    user_id: Optional[str] = None
    task_types: List[str]
    priority: Optional[int] = None
