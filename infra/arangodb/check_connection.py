from arango import ArangoClient


def check_arango_connection():

    # Initialize the ArangoDB client
    client = ArangoClient(hosts="http://localhost:8529")

    # Connect to "_system" database as root user
    try:
        sys_db = client.db("_system", username="root", password="rootpassword")
        # Attempt to list collections as a way to check the connection
        collections = sys_db.collections()
        print("Successfully connected to ArangoDB!")
        print(collections)
    except Exception as e:
        print(f"Failed to connect to ArangoDB. Error: {e}")


if __name__ == "__main__":
    check_arango_connection()
