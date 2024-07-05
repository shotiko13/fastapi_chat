from connection import get_database
import bcrypt
from pymongo.errors import PyMongoError
from connection import MongoConnector

class UserRepository:

    def __init__(self) -> None:
        self.connection = MongoConnector()
        self.connection.create_index("username")

    def register_user(self, username, password) -> dict[str, str]:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            self.connection.db.insert_one({
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
        user = self.connection.db.find_one({"username": username})
        return user

user_repository = UserRepository()