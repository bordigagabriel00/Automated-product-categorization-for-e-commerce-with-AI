import logging
from typing import Dict, Optional
from arango import ArangoClient, ArangoError


class ArangoDBConnection:
    _instances: Dict[str, 'ArangoDBConnection'] = {}

    def __init__(self, hosts: str, username: str, password: str, database: str):
        self.client = ArangoClient(hosts=hosts)
        self._db_name = database
        try:
            self.db = self.client.db(database, username=username, password=password)
            logging.info("DB: Successfully connected to the database.")
        except ArangoError as e:
            logging.error(f"DB: Failed to connect to the database: {e}")
            raise

    @classmethod
    def get_instance(cls, hosts: str, username: str, password: str, database: str) -> 'ArangoDBConnection':

        instance_key = f"{hosts}-{username}-{database}"

        if instance_key not in cls._instances:
            if not all([hosts, username, password, database]):
                raise ValueError("DB: All connection details must be provided for the first initialization!")
            cls._instances[instance_key] = cls(hosts, username, password, database)

        return cls._instances[instance_key]

    def get_connection(self):
        return self.db

    def verify_connection(self) -> bool:
        try:
            # This effectively checks if the specific database is accessible
            self.db.collections()
            logging.info("DB: Connection to ArangoDB is successful.")
            return True
        except ArangoError as e:
            logging.error(f"DB: Error verifying connection to ArangoDB: {e}")
            return False
