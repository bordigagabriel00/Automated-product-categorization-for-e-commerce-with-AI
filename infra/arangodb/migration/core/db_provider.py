import logging

from arango.exceptions import ArangoError

from core.arangodb_provider import ArangoDBConnection
from config import settings

DB_NAME = "Product_Model"


def init_database(db: ArangoDBConnection):
    try:
        db_sys = db.get_instance(settings.arango_url,
                                 settings.username,
                                 settings.password,
                                 settings.name_system_db).get_connection()

        # Check if the database exists
        if not db_sys.has_database(DB_NAME):
            logging.info(f"The database '{DB_NAME}' does not exist. Creating it...")
            # Create the database
            db_sys.create_database(DB_NAME)
            logging.info(f"Database '{DB_NAME}' successfully created.")

        else:
            logging.info(f"The database '{DB_NAME}' already exists.")

        return True

    except ArangoError as e:
        logging.error(f"An error occurred with ArangoDB: {e}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return False
