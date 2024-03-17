import pandas as pd
import logging
from requests import Response

from core.arangodb_provider import ArangoDBConnection
from config import settings
from core.db_provider import DB_NAME  # Correct the typo in the import

MANUFACTURER_COL = "manufacturer"


async def init_manufacturer_type(data, model_db: ArangoDBConnection):
    try:
        # Convert JSON response to DataFrame
        logging.info("DB: Processing manufacturer.")
        product = pd.json_normalize(data)

        # Get distinct types
        manufacturer_set = product['manufacturer'].dropna().unique()

        db = model_db.get_instance(settings.arango_url,
                                   settings.username,
                                   settings.password,
                                   DB_NAME).get_connection()

        # Check if 'manufacturer' collection exists
        logging.info("DB: Checking manufacturer collection")
        if not db.has_collection(MANUFACTURER_COL):
            logging.info("DB: Creating the manufacturer collections.")
            db.create_collection(MANUFACTURER_COL)

        logging.info("DB: Get manufacturer collection")
        manufacturer_collection = db.collection(MANUFACTURER_COL)

        # Insert distinct manufacturers with id and name
        logging.info("DB: Updating the manufacturer data.")
        for index, manufacturer_type in enumerate(manufacturer_set, start=1):
            if not manufacturer_collection.find({'name': manufacturer_type}).count():
                manufacturer_collection.insert({'_key': str(index), 'name': manufacturer_type})

        logging.info("DB: Ending the manufacturer data.")
        return True
    except Exception as e:
        logging.error(f"Error initializing manufacturer type: {e}")
        return False
