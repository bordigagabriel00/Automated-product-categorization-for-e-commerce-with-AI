import logging

import requests

from config import settings
from core.arangodb_provider import ArangoDBConnection
from core.type_provider import create_product_type

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_data_from_url():
    # Fetch data from URL
    resp = requests.get(settings.product_url)
    if resp.status_code != 200:
        logging.error(f"Failed to retrieve data. Status code: {resp.status_code}")
        return False, resp

    return True, resp


if __name__ == "__main__":
    # Get data source
    ok, response = get_data_from_url()
    if not ok:
        logging.error("Import: The url is invalid")

    # Verify connection
    try:
        db_connection = ArangoDBConnection.get_instance(settings.arango_url,
                                                        settings.username,
                                                        settings.password,
                                                        settings.name_system_db)

        if db_connection.verify_connection():
            logging.info("DB: The ArangoDB connection is active and verified.")
        else:
            logging.error("DB: The ArangoDB connection could not be verified.")
    except Exception as e:
        logging.error(f"Failed to initialize ArangoDB connection: {e}")

    if not create_product_type(response):
        logging.error("Error initializing the product type")

# the port is defined by command


"""
TODO: Nove Type
TODO: Manufacturer
TODO: Pipeline
TODO: Predict
TODO: Products
"""
