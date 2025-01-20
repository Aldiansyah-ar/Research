from pymongo import MongoClient

def save_to_mongodb(data, db_config, collection_name):
   client = MongoClient(db_config['host'], db_config['port'])
   db = client[db_config['db_name']]
   collection = db[collection_name]

   if data:
      collection.insert_many(data)
   client.close()

# Konfigurasi database MongoDB
db_config = {
    'db_name': 'dbname',
    'host': 'localhost',
    'port': 27017
}