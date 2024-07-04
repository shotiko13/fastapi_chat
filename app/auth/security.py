from fastapi import Depends, HTTPException, status
from .config import SECRET_KEY, ALGORITHM
from .models import TokenData
from .jwt import decode_token
from .models import User

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "password": "secret"
    }
}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    print(token)
    if payload is None:
        raise credentials_exception
    
    print(payload)
    token_data = TokenData(**payload)
    return token_data

def verify_password(plain, hashed):
    return plain == hashed

def get_user(db, username: str):
    user = db.get(username)
    if user:
        return User(**user)
    return None

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        return False
    return True