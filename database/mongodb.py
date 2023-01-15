import logging
import sys

from motor.motor_asyncio import AsyncIOMotorClient


async def connect_mongodb(MONGO_URI: str) -> None:
    try:
        mongodb = AsyncIOMotorClient(MONGO_URI)
        await mongodb.server_info()
    except:
        logging.error(
            "Can't connect to MongoDB: invalid URI")
        sys.exit()
