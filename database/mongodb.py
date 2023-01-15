import logging
import sys

from motor.motor_asyncio import AsyncIOMotorClient

from config import config


class MongoCollection:

    def __init__(self, collection):
        self.collection = collection

    async def read_document(self, document_id):
        """
        Read the document by document ID.
        """
        return await self.collection.find_one({"_id": document_id})

    async def update_document(self, document_id, updated_data):
        """
        Update (or create if not exists) document by document ID.
        """
        updated_data = {"$set": updated_data}
        await self.collection.update_one({"_id": document_id}, updated_data, upsert=True)

    async def delete_document(self, document_id):
        """
        Delete document by document ID.
        """
        await self.collection.delete_one({'_id': document_id})

    async def total_documents(self):
        """
        Return total number of documents in this collection.
        """
        return await self.collection.count_documents({})

    async def get_all_ids(self):
        """
        Return list of all document IDs in this collection.
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
