from pymongo import MongoClient
from configuration.config import DATABASE_NAME, CONNECTION_STRING

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client

def create_uri(config):

    username = config.get("username")
    password = config.get("password")

    credentials = ""

    if username and password:
        credentials = f"{username}:{password}@"

    uri = "mongodb://{credentials}{host}:{port}/{name}".format(
        credentials=credentials, **config
    )

    return uri


class MongoConnector:
    def __init__(self, **config):
        self.client = get_database()
        self.db = self.client[DATABASE_NAME]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self, **kwargs):
        self.client.close()

    def update_one(self, selector, collection, data):
        self.db[collection].update_one(selector, {"$set": data}, upsert=True)

    def create_index(self, collection, name):
        return self.db[collection].create_index([(name, 1)])

    def info_index(self, collection):
        return self.db[collection].index_information()
