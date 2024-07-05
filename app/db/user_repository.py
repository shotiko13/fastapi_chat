import bcrypt
from pymongo.errors import PyMongoError
from pymongo import ASCENDING
from .connection import connector

class UserRepository:

    def __init__(self) -> None:
        self.collection = connector.db["users"]
        connector.create_index("users", "username", unique=True)

    def register_user(self, username, password) -> dict[str, str]:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            self.collection.insert_one({
            "username": username,
            "password": hashed_password,
        })
        except PyMongoError:
            return {
                "message": "Error adding in the database"
            }
        return {
            "message": "user registered successfully",
        }

    def verify_unique_user(self, username) -> bool:
        pass
    
    def find_user(self, username):
        user = self.collection.find_one({"username": username})
        return user

user_repository = UserRepository()