from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from users.DAO import UsersDAO
from users.schemas import SUser
from jose import JWTError, jwt
from config import settings
from fastapi import Depends, HTTPException, Request, Response, status
from tasks.DAO import DAO

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
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc),"type": "access"})
    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY.get_secret_value(), 
                             algorithm=settings.ALGORITHM.get_secret_value())
    return encoded_jwt

def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc),"type": "refresh"})
    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY.get_secret_value(), 
                             algorithm=settings.ALGORITHM.get_secret_value())
    return encoded_jwt


def validate_tokens(request:Request, response: Response):
    access = request.cookies.get("todo_at")
    if not access:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="access token does not exist")
    try:
        payload = jwt.decode(token=access, 
                                key=settings.SECRET_KEY.get_secret_value(), 
                                algorithms=[settings.ALGORITHM.get_secret_value()])
        user =  payload["sub"]     
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user is invalid")
        return user
    except JWTError as e:
        refresh = request.cookies.get("todo_rt")
        if not refresh:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token does not exist")
        try:
            payload = jwt.decode(token=refresh, 
                                key=settings.SECRET_KEY.get_secret_value(), 
                                algorithms=[settings.ALGORITHM.get_secret_value()])
            access_token = create_access_token({"sub":payload["sub"]})
            refresh_token = create_refresh_token({"sub":payload["sub"]})
            response.set_cookie("todo_at",
                            access_token,
                            httponly=True
                            )
            response.set_cookie("todo_rt",
                            refresh_token,
                            httponly=True
                            )
            user =  payload["sub"]     
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user is invalid")
            return user
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authirze again")
    