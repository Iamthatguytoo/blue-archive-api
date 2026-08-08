from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from datetime import datetime, timezone
from pymongo import ReturnDocument
from db.database_async import api_key_collection
import hashlib


scrt_api_key = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_key(api_key: str = Security(scrt_api_key)):
    if not api_key:
        raise HTTPException(status_code=403, detail="API key required")

    today = datetime.now(timezone.utc).date().isoformat()

    api_key = hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    key_doc = await api_key_collection.find_one({"hashed_api_key": api_key})

    if not key_doc:
        raise HTTPException(status_code=403, detail="Invalid API key")

    if key_doc["resetted_at"] != today:
        await api_key_collection.update_one(
            {"_id": key_doc["_id"], "resetted_at": {"$ne": today},},
            {"$set": {"requests_today": 0, "resetted_at": today,}},
        )

        key_doc = await api_key_collection.find_one({"_id": key_doc["_id"]})

    result = await api_key_collection.find_one_and_update(
        {"_id": key_doc["_id"], "requests_today": {"$lt": key_doc["daily_limit"]}},
        {"$inc": {"requests_today": 1}},
        return_document=ReturnDocument.AFTER,
    )

    if not result:
        raise HTTPException(
            status_code=429,
            detail=f"Daily limit exceeded for {key_doc['tier']} tier. {key_doc['tier']} tier only gives {key_doc['daily_limit']} requests/day.",
        )

    return result
