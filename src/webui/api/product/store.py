# store.py
from arango import ArangoClient

# Setup client and database
# TODO: FIXME Use settings
client = ArangoClient(hosts='http://localhost:8529')
db = client.db('your_db_name', username='root', password='your_password')


class ItemStore:
    def create_product(self, item):
        return db.collection('items').insert(item.dict())

    def get_product(self, item_id):
        return db.collection('items').get(item_id)

    def update_product(self, item_id, item):
        return db.collection('items').update({'_key': item_id, **item.dict()})

    def delete_product(self, item_id):
        return db.collection('items').delete(item_id)
