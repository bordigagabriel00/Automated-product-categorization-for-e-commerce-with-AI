import pandas as pd
import logging
from requests import Response

from config import settings
from core.arangodb_provider import ArangoDBConnection
from core.db_provider import DB_NAME

PRODUCT_COL = "product"


async def init_product(data, model_db: ArangoDBConnection):
    try:
        # Convert JSON response to DataFrame
        logging.info("DB: Processing product type data")

        db = model_db.get_instance(settings.arango_url,
                                   settings.username,
                                   settings.password,
                                   DB_NAME).get_connection()

        # Check if 'product' collection exists
        logging.info("DB: Checking product data")
        if not db.has_collection(PRODUCT_COL):
            logging.info("DB: Creating the product data.")
            db.create_collection(PRODUCT_COL)

        logging.info("DB: Getting product data")
        product_ref = db.collection(PRODUCT_COL)

        # Insert distinct types with id and name
        logging.info("DB: Updating the product data.")
        try:
            result = product_ref.import_bulk(documents=data, on_duplicate="update")
            logging.info(
                f"Inserted {result['created']} products, updated {result['updated']}, errors {result['errors']}.")
        except Exception as e:
            logging.error(f"Failed to insert products: {e}")

        logging.info("DB: Ending product data")
        return True
    except Exception as e:
        logging.error(f"Error initializing product: {e}")
        return False


