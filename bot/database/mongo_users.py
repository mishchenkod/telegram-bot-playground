from datetime import datetime, timezone

from telegram import User

from database import mongo


async def save_user(user: User):
    """
    Save new user to MongoDB.
    """
    document_data = {
        "username": user.username,
        "name": (user.first_name or " ") + (user.last_name or ""),
        "date": datetime.now(timezone.utc)}
    await mongo.users.update(user.id, document_data)


async def find_user(id: int) -> dict:
    """
    Find user by user ID.
    """
    return await mongo.users.find(id)


async def get_all_user_ids():
    """
    Get all saved user IDs.
    """
    user_ids = []
    for document_id in await mongo.users.get_all_ids():
        user_ids.append(document_id)
    return user_ids
