import logging
import sys

from config import config
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


class MongoCollection:

    def __init__(self, collection):
        self.collection = collection

    async def find(self, document_id):
        """
        Find document by document ID.
        """
        return await self.collection.find_one({"_id": document_id})

    async def update(self, document_id, document_data):
        """
        Update or create document by document ID.
        """
        document_data = {"$set": document_data}
        await self.collection.update_one({"_id": document_id}, document_data, upsert=True)

    async def delete(self, document_id):
        """
        Delete document by document ID.
        """
        await self.collection.delete_one({'_id': document_id})

    async def count(self):
        """
        Get total number of documents in this collection.
        """
        return await self.collection.count_documents({})

    async def get_all_ids(self):
        """
        Get list of all document IDs in this collection.
        """
        return await self.collection.distinct("_id")


async def check_connection(uri: str) -> None:
    try:
        logging.info("MongoDB URI: " + uri)
        mongodb = AsyncIOMotorClient(uri)
        await mongodb.server_info()
    except:
        logging.error(
            "Can't connect to MongoDB: invalid URI")
        sys.exit()

mongo = AsyncIOMotorClient(config.MONGO_URI)
database = mongo.bot

users = MongoCollection(database.users)
chats = MongoCollection(database.chats)
