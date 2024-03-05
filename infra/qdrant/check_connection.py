from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionDescription, FieldIndex, Filter, PointStruct

def create_collection(client, collection_name):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config={
            "size": 4, # Adjust based on your vector size
            "distance": "Cosine" # Or "Euclidean", based on your requirements
        },
        payload_schema={
            "name": "keyword",
            "description": "text",
        }
    )
    print(f"Collection '{collection_name}' created.")

def insert_product(client, collection_name, product_id, vector, payload):
    client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=product_id, vector=vector, payload=payload)]
    )
    print(f"Product {payload['name']} inserted.")

def update_product(client, collection_name, product_id, payload):
    client.update(
        collection_name=collection_name,
        point_id=product_id,
        payload=payload
    )
    print(f"Product {product_id} updated.")

def delete_product(client, collection_name, product_id):
    client.delete(
        collection_name=collection_name,
        point_id=product_id,
    )
    print(f"Product {product_id} deleted.")

if __name__ == "__main__":
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "products"

    # Create a collection
    create_collection(client, collection_name)

    # Insert a product
    insert_product(client, collection_name, 1, [0.1, 0.2, 0.3, 0.4], {"name": "Product 1", "description": "A sample product"})

    # Update the product
    update_product(client, collection_name, 1, {"description": "An updated sample product"})

    # Delete the product
    delete_product(client, collection_name, 1)
