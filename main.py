# main.py
import uvicorn
from fastapi import FastAPI
from match import fetch_and_store_data
from database import get_fixture_ids
from config import Settings
import logging

app = FastAPI()
settings = Settings()
logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
async def startup_event():
    fixture_ids = await get_fixture_ids()
    logging.info(f"There will be {len(fixture_ids)} API calls.")
    logging.info(fixture_ids)
    if fixture_ids:
        for fixture_id in fixture_ids:
            logging.info(f"Fetching data for fixture ID: {fixture_id}")
            data = await fetch_and_store_data("euro-2024-matches", fixture_id)
            logging.info(f"Response data for fixture ID {fixture_id}: {data}")


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
