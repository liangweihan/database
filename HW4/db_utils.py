from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017/", db_name='hw3', collection_name='testCollection'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_all_items(self):
        return list(self.collection.find())

    def get_item_by_id(self, id):
        try:
            return self.collection.find_one({'_id': ObjectId(id)})
        except:
            return None

    def insert_item(self, item):
        self.collection.insert_one(item)

    def update_item(self, id, updated_data):
        self.collection.update_one({'_id': ObjectId(id)}, {'$set': updated_data})

    def delete_item(self, id):
        result = self.collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0
