import asyncio
import json
import logging
import sys
from typing import Any

import aiohttp

from config import settings
from core.arangodb_provider import ArangoDBConnection
from core.db_provider import init_database, DB_NAME
from core.manufacturer_provider import init_manufacturer_type
from core.type_provider import init_product_type

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def get_data_from_url():
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.product_url) as resp:
            if resp.status != 200:
                logging.error(f"Failed to retrieve data. Status code: {resp.status}")
                return False, None  # Return None or appropriate value for response

            text = await resp.text()  # Get response text
            try:
                data = json.loads(text)  # Manually parse JSON
                return True, data
            except json.JSONDecodeError:
                logging.error("Failed to decode JSON")
                return False, None


async def main():
    db_sys = Any
    model_db = Any

    # Get data source
    logging.info("DB: Get data from URL")
    ok, response = await get_data_from_url()
    if not ok:
        sys.exit("Import: The url is invalid")

    # Verify connection system database
    logging.info("DB: verify connection system database")
    try:
        db_sys = ArangoDBConnection.get_instance(settings.arango_url,
                                                 settings.username,
                                                 settings.password,
                                                 settings.name_system_db)

        if db_sys.verify_connection():
            logging.info("DB: The ArangoDB connection is active and verified.")
        else:
            logging.error("DB: The ArangoDB connection could not be verified.")
    except Exception as e:
        sys.exit(f"Failed to initialize ArangoDB connection: {e}")

    if not init_database(db_sys):
        sys.exit("Error initializing the product model")

    # Verify connection model database
    logging.info("DB: verify connection model database")
    try:
        model_db = ArangoDBConnection.get_instance(settings.arango_url,
                                                   settings.username,
                                                   settings.password,
                                                   DB_NAME)

        if model_db.verify_connection():
            logging.info("DB: The ArangoDB connection is active and verified.")
        else:
            sys.exit("DB: The ArangoDB connection could not be verified.")
    except Exception as e:
        sys.exit(f"Failed to initialize ArangoDB connection: {e}")

    # Initialize collections
    tasks = [
        asyncio.create_task(init_product_type(response, model_db)),
        asyncio.create_task(init_manufacturer_type(response, model_db))
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Check if any of the tasks failed
    if any(not result for result in results):
        sys.exit("Error initializing collections")


if __name__ == "__main__":
    asyncio.run(main())

"""
TODO: Nove Type
TODO: Manufacturer
TODO: Pipeline
TODO: Predict
TODO: Products
"""
