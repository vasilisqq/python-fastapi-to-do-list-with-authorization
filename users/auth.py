from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from users.DAO import UsersDAO
from users.schemas import SUser
from jose import JWTError, jwt
from config import settings
from fastapi import Depends, HTTPException, Request, status

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


def get_token(request:Request):
    token = request.cookies.get('todo_at')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token=token, 
                                key=settings.SECRET_KEY.get_secret_value(), 
                                algorithms=[settings.ALGORITHM.get_secret_value()])
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    return user_id