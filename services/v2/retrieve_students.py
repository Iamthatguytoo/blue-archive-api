from db.database_async import student_collection
from utils.serialize_students import serialize_student
from pydantic import BaseModel
import re


async def fetch_students(
    filters: BaseModel,
    name: str | None = None,
    base_name: str | None = None,
    limit: int = 20,
    skip: int = 0,
):
    query = {}

    if name:
        query["name"] = {"$regex": f"^{re.escape(name)}$", "$options": "i"}
    if base_name:
        exact_query = {
            "base_name": {"$regex": f"^{re.escape(base_name)}$", "$options": "i"}
        }

        count = await student_collection.count_documents(exact_query)

        if count:
            query.update(exact_query)
        else:
            query["base_name"] = {"$regex": re.escape(base_name), "$options": "i"}

    query.update(filters.model_dump(exclude_none=True))

    total = await student_collection.count_documents(query)

    cursor = student_collection.find(query).skip(skip).limit(limit)

    students = await cursor.to_list(length=limit)

    students = [serialize_student(s) for s in students]

    return {"total": total, "skip": skip, "limit": limit, "students": students}
