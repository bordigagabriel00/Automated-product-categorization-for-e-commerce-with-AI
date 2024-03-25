import pandas as pd
import logging
from requests import Response

from config import settings
from core.arangodb_provider import ArangoDBConnection
from core.db_provider import DB_NAME

PRODUCT_TYPE_COL = "product_type"


async def init_product_type(data, model_db: ArangoDBConnection):
    try:
        # Convert JSON response to DataFrame
        logging.info("DB: Processing product type data")
        product = pd.json_normalize(data)

        # Get distinct types
        types_set = product['type'].dropna().unique()

        db = model_db.get_instance(settings.arango_url,
                                   settings.username,
                                   settings.password,
                                   DB_NAME).get_connection()

        # Check if 'product_type' collection exists
        logging.info("DB: Checking product type data")
        if not db.has_collection(PRODUCT_TYPE_COL):
            logging.info("DB: Creating the product type data.")
            db.create_collection(PRODUCT_TYPE_COL)

        logging.info("DB: Getting product type data")
        types_collection = db.collection(PRODUCT_TYPE_COL)

        # Insert distinct types with id and name
        logging.info("DB: Updating the product type data.")
        for index, product_type in enumerate(types_set, start=1):
            if not types_collection.find({'name': product_type}).count():
                types_collection.insert({'_key': str(index), 'name': product_type})

        logging.info("DB: Ending product type data")
        return True
    except Exception as e:
        logging.error(f"Error initializing product type: {e}")
        return False
