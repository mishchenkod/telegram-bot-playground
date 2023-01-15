from database import mongodb
from datetime import datetime, timezone


async def save_user(user):
    """
    Save new user in the database.
    """
    insert_format = {
        "username": user.username,
        "name": (user.first_name or " ") + (user.last_name or ""),
        "date": datetime.now(timezone.utc)}
    await mongodb.users.update_document(user.id, insert_format)
