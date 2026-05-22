from pymongo import MongoClient
import os

env_client = os.getenv("CLIENT")
env_db = os.getenv("DATABASE")
env_collection = os.getenv("API_COLLECTION")
env_collection_keys = os.getenv("API_COLLECTION_KEYS")

client = MongoClient(env_client)
db = client[env_db]
student_collection = db[env_collection]
api_key_collection = db[env_collection_keys]

"""
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env.local" 

load_dotenv(env_path, override=True)
"""
