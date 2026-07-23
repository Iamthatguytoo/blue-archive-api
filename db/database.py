from pymongo import MongoClient
from db.settings import settings

client = MongoClient(settings.CLIENT, tz_aware=True)
db = client[settings.DATABASE]

student_collection = db[settings.API_COLLECTION]
api_key_collection = db[settings.API_COLLECTION_KEYS]
scraper_collection = db[settings.API_COLLECTION_SCRAPER]