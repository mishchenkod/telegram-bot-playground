import logging
import sys

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from bot.config import config
from bot.database.potd import PersonOfTheDayGame


async def initialize_database() -> None:
    try:
        logging.info("MongoDB URI: " + config.MONGO_URI)
        client = AsyncIOMotorClient(config.MONGO_URI)
        await client.server_info()
        await init_beanie(database=client.bot, document_models=[PersonOfTheDayGame])
    except:
        logging.error(
            "Can't connect to MongoDB: invalid URI")
        sys.exit()
