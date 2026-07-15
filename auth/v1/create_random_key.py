from db.database import api_key_collection
from datetime import datetime, timezone
import secrets

def generate_key(tier = "free"):
    limits = {
        "free": {"daily_limit": 1000},
    }

    rate = limits[tier]["daily_limit"]
    

    while True:
        api_key = "sk_" + secrets.token_hex(16)
        if not api_key_collection.find_one({"api_key": api_key}):
            break

    today = datetime.now(timezone.utc).date().isoformat()
 
    data = {
        "api_key": api_key,
        "daily_limit": rate,
        "tier": tier,
        "requests_today": 0,
        "resetted_at": today,
        "created_at": datetime.now(timezone.utc),
    }
        
    api_key_collection.insert_one(data)

    return {
        "api_key": data["api_key"],
        "daily_limit": data["daily_limit"],
        "tier": data["tier"],
        "resetted_at": today,
    }
    