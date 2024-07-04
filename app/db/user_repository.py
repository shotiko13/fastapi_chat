from connection import get_database
import bcrypt
from pymongo.errors import PyMongoError

class UserRepository:

    try:
        db = get_database()
        collection = db["users"]
    except PyMongoError as e:
        print(f"Database connection error: {e}")

    @classmethod
    def register_user(cls, username, password) -> dict[str, str]:
        if cls.verify_unique_user(username):
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            try:
                cls.collection.insert_one({
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
        else:
            return {
                "message": "username already exists in the database"
            }

    @classmethod
    def verify_unique_user(cls, username) -> bool:
        try:
            user = cls.collection.find_one({"username": username})
        except PyMongoError:
            return {
                "Message": "error querying for user"
            }
        return user is None
