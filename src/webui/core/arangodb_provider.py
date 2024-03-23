from typing import Optional

from arango import ArangoClient
from core.logger_provider import logger


class ArangoDBConnection:
    _instance: Optional['ArangoDBConnection'] = None

    def __init__(self, hosts: str, username: str, password: str, database: str):
        if ArangoDBConnection._instance is not None:
            raise Exception("DB: This class is a singleton and has already been instantiated!")
        else:
            self.client = ArangoClient(hosts=hosts)
            self.db = self.client.db(database, username=username, password=password)
            ArangoDBConnection._instance = self

    @classmethod
    def get_instance(cls, hosts: str = "", username: str = "", password: str = "",
                     database: str = "") -> 'ArangoDBConnection':
        if cls._instance is None:
            if not all([hosts, username, password, database]):
                raise ValueError("DB: All connection details must be provided for the first initialization!")
            cls(hosts, username, password, database)
        return cls._instance

    def get_connection(self):
        return self.db

    def verify_connection(self) -> bool:
        try:
            # Attempt to list databases as a connection check
            self.client.db()
            logger.info("DB: Connection to ArangoDB is successful.")
            return True
        except Exception as e:
            logger.error(f"DB: Error connecting to ArangoDB: {e}")
            return False
