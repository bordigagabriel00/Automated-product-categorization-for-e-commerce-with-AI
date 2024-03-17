import logging

import pandas as pd
import requests

from config import settings
from core.arangodb_provider import ArangoDBConnection


def create_product_type():
    # Fetch data from URL
    response = requests.get(settings.product_url)
    if response.status_code != 200:
        logging.error("Failed to retrieve data")
        return False

    # Convert JSON response to DataFrame
    product = pd.json_normalize(response.json())

    # Get distinct types
    types_set = product['type'].dropna().unique()

    conn = ArangoDBConnection.get_instance().get_connection()

    # Check if 'types' collection exists
    if not conn.has_collection('types'):
        conn.create_collection('types')

    types_collection = conn.collection('types')

    # Insert distinct types with id and name
    for index, product_type in enumerate(types_set, start=1):
        if not types_collection.find({'name': product_type}):
            types_collection.insert({'id': index, 'name': product_type})

    return True
