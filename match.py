# match.py
import requests
import asyncio
from fastapi import HTTPException
from database import get_collection
from config import Settings
import logging

settings = Settings()
logging.basicConfig(level=logging.INFO)


async def fetch_and_store_data(collection_name, fixture_id):
    try:
        await asyncio.sleep(5)
        url = f"{settings.API_FOOTBALL_URL}{settings.FIXTURES}?id={fixture_id}"
        response = requests.get(url, headers=settings.API_HEADERS)
        response.raise_for_status()
        data = response.json()['response']
        if data:
            collection = await get_collection(collection_name)
            for item in data:
                await collection.update_one(
                    {"fixture.id": fixture_id},
                    {"$set": item},
                    upsert=True
                )
            logging.info(f"Data for fixture ID {fixture_id} has been updated/inserted.")
        else:
            logging.info(f"No data found for fixture ID: {fixture_id}")
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching data for fixture ID {fixture_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
