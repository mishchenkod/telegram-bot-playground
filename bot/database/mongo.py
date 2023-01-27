import logging
import sys

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from bot.config import config
from bot.models.chat_user import ChatUser


async def check_connection(uri: str) -> None:
    try:
        logging.info("MongoDB URI: " + uri)
        mongodb = AsyncIOMotorClient(uri)
        await mongodb.server_info()
    except:
        logging.error(
            "Can't connect to MongoDB: invalid URI")
        sys.exit()


async def initialize() -> None:
    client = AsyncIOMotorClient(config.MONGO_URI)
    await init_beanie(database=client.bot, document_models=[ChatUser])
