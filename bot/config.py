"""Environment variables and configuration constants"""
from os import getenv

from dotenv import load_dotenv

load_dotenv(".env")

TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
MONGO_URI = getenv("MONGO_URI")
