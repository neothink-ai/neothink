import openai
import os
from typing import List
from datetime import datetime
import json

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai.api_key = api_key

async def generate_tasks_from_description(description: str) -> List[dict]:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a project management assistant. 
                Create tasks in JSON format with these fields: title, description, priority (Low/Medium/High), 
                size (Small/Medium/Large). Return only the JSON array."""},
                {"role": "user", "content": f"Create tasks for this project: {description}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract the content and parse JSON
        content = response.choices[0].message.content
        # Clean the content to ensure it's valid JSON
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:-3]  # Remove ```json and ``` markers
        
        tasks = json.loads(content)
        
        # Format tasks with required fields
        formatted_tasks = []
        for task in tasks:
            formatted_task = {
                "title": task["title"],
                "description": task["description"],
                "priority": task.get("priority", "Medium"),
                "size": task.get("size", "Medium"),
                "state": "todo",
                "columnId": "todo",
                "created_time": datetime.now().isoformat(),
                "deadline": None,
                "assignee": None,
                "assigned_time": None,
                "completed_time": None
            }
            formatted_tasks.append(formatted_task)
            
        return formatted_tasks
        
    except Exception as e:
        print(f"Error in generate_tasks_from_description: {str(e)}")
        raise Exception(f"Failed to generate tasks: {str(e)}")
