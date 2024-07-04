from pymongo import MongoClient
from configuration.config import DATABASE_NAME, CONNECTION_STRING

def get_database():
    client = MongoClient(CONNECTION_STRING)
    return client[DATABASE_NAME]
