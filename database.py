# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure environment variables are loaded and are strings
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Validate that the environment variables are not empty
if not username or not password:
    raise ValueError("DB_USERNAME and DB_PASSWORD must be set in the environment variables")

# Quote the username and password to handle special characters
username = quote_plus(username)
password = quote_plus(password)

MONGODB_URI = f"mongodb+srv://{username}:{password}@cluster0.gffqhng.mongodb.net/"
client = AsyncIOMotorClient(MONGODB_URI)


async def get_collection(collection_name):
    db_name = "football"
    db = client[db_name]
    return db[collection_name]


async def get_fixture_ids():
    collection = await get_collection("euro-24-fixture")
    fixture_ids = [doc["fixture"]["id"] for doc in await collection.find({}, {"fixture.id": 1}).to_list(length=None)]
    return fixture_ids
