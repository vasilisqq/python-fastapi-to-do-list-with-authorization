from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
from users.DAO import UsersDAO
from users.schemas import SUser
from jose import jwt
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def auth_user(username: str, password:str) -> None|SUser:
    user = await UsersDAO.find_existing(username)
    if not user and not verify_password(password, user.password):
        return None
    return user

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY.get_secret_value(), 
                             algorithm=settings.ALGORITHM.get_secret_value())
    return encoded_jwt