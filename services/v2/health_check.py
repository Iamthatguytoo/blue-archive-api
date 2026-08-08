from db.database_async import client
from db.settings import settings
from pymongo.errors import PyMongoError
from fastapi import HTTPException
from datetime import datetime, UTC
from time import time

START = time()


async def create_health_check():
    timestamp = datetime.now(UTC)
    try:
        await client.admin.command("ping")

        uptime = int(time() - START)

        return {
            "status": "healthy",
            "version": "2.1.0",
            "uptime": uptime,
            "connection_checks": {
                "mongodb": True,
            },
            "timestamp": timestamp.isoformat(),
            "environment": settings.ENVIRONMENT,
        }

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "version": "2.1.0",
                "connection_checks": {
                    "mongodb": False,
                },
                "timestamp": timestamp.isoformat(),
                "environment": settings.ENVIRONMENT,
            },
        )
