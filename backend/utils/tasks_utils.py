from database import Database
from bson.objectid import ObjectId

db = Database.get_db()
tasks_collection = db["Tasks"]["tasks"]

def create_task(task_data):
    return tasks_collection.insert_one(task_data).inserted_id

def get_tasks_by_user(userid):
    return list(tasks_collection.find({"userid": userid}))

def update_task(task_id, updated_data):
    return tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_data})

def delete_task(task_id):
    return tasks_collection.delete_one({"_id": ObjectId(task_id)})