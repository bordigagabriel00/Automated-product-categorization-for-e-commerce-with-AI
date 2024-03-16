import pandas as pd
from requests import Response

from core.arangodb_provider import ArangoDBConnection


# noinspection DuplicatedCode
def create_product_type(response: Response):
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
