def insert_unique_document(collection, document, unique_field):
    exists = collection.find({unique_field: document[unique_field]}).count() > 0
    if not exists:
        collection.insert(document)