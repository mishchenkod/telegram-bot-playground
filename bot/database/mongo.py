"""Database connection and configuration"""
import logging

import beanie
from motor.motor_asyncio import AsyncIOMotorClient

from bot import config
from bot.services.potd import PersonOfTheDayGame


async def initialize_database() -> None:
    """Initializes MongoDB connection"""
    logging.info("MongoDB URI: %s", config.MONGO_URI)
    client = AsyncIOMotorClient(config.MONGO_URI)
    await client.server_info()
    await beanie.init_beanie(database=client.bot, document_models=[PersonOfTheDayGame])
