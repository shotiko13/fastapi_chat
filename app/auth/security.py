from fastapi import Depends, HTTPException, status
from ..configuration.config import SECRET_KEY, ALGORITHM
from ..db.models import TokenData
from .jwt import decode_token
from ..db.models import User
from db.user_repository import user_repository

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    user = user_repository.find_user(username)
    if not user or not verify_password(password, user["password"]):
        return False
    return True