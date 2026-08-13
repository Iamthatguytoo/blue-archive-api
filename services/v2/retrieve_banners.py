from db.database_async import banner_collection
from utils.serializers import serialize_banner

async def get_current_banners():
    cursor = banner_collection.find({})
    result = await cursor.to_list(length=None)

    result = [serialize_banner(banner) for banner in result]

    return {
        "banners": result
    }