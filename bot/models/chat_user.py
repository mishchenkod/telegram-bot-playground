from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from bot.database import mongo


class ChatUser(Document):
    user_id: int
    chat_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    last_update: datetime

    class Settings:
        name = "users"
