import logging

from config import settings
from core.arangodb_provider import ArangoDBConnection
from core.db_provider import DB_NAME

CATEGORY_COL = "category"


async def init_category_type(data, model_db: ArangoDBConnection):
    try:
        logging.info("DB: Processing category data")

        # Get the database connection
        db = model_db.get_instance(settings.arango_url,
                                   settings.username,
                                   settings.password,
                                   DB_NAME).get_connection()

        logging.info("DB: Checking category collection")
        # Ensure the collection exists
        if not db.has_collection(CATEGORY_COL):
            db.create_collection(CATEGORY_COL)

        category_col_ref = db.collection(CATEGORY_COL)

        # Extract and process unique categories
        unique_categories = {cat['id']: cat for item in data for cat in item.get('category', [])}

        for cat_id, category in unique_categories.items():
            doc = {'_key': cat_id, 'name': category['name']}
            if not category_col_ref.get(cat_id):
                try:
                    # Insert the category if it does not exist
                    category_col_ref.insert(doc)
                    logging.info(f"Category '{category['name']}' successfully inserted.")
                except Exception as e:
                    logging.error(f"Error inserting category {category['name']}: {e}")
            else:
                logging.info(f"Category with ID {cat_id} already exists, skipping insertion.")

        logging.info("DB: Finished processing category data.")
        return True

    except Exception as e:
        logging.error(f"Error initializing categories: {e}")
        return False
