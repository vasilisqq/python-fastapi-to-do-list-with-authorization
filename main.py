from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings
from users.router import router as users_router

SECRET_KEY=settings.SECRET_KEY.get_secret_value()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30





# class Token(BaseModel):
#     acces_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str|None = None


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.include_router(users_router)

# def create_access_token(data:dict, expires_delta: timedelta|None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# async def get_current_user(token:str = Depends(oauth_2_scheme)):
#     credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error", headers={"WWW-Authenticate": "Bearer"})
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credential_exception
#         token_data = TokenData(username)
#     except JWTError:
#         raise credential_exception
#     user = username
#     if user is None:
#         raise credential_exception
#     return user