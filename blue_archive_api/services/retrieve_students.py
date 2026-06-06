from db.database import student_collection
from pydantic import BaseModel
import re

def serialize_student(doc: dict) -> dict:
    doc = dict(doc)
    doc.pop("_id", None)
    if "class" in doc:
        doc["class_name"] = doc.pop("class")
    return doc

def fetch_students( filters: BaseModel, name: str | None = None, base_name: str | None = None, limit: int = 20, skip: int = 0):
    query = {}
    
    if name:
        query['name'] = {"$regex": f"^{re.escape(name)}$", "$options": "i"}
        
    if base_name:
        exact_query = {"base_name": {"$regex": f"^{re.escape(base_name)}$", "$options": "i"}}

        count = student_collection.count_documents(exact_query)

        if count:
            query.update(exact_query)
        else:
            query['base_name'] = {"$regex": re.escape(base_name), "$options": "i"}
            
    query.update(filters.model_dump(exclude_none=True))

    total = student_collection.count_documents(query)

    student_cursor = (student_collection.find(query).skip(skip).limit(limit))

    students = [serialize_student(s) for s in student_cursor]

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "students": students
    }
