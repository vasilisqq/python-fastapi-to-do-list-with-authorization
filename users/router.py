from fastapi import APIRouter, Depends, Response
from users.schemas import SUser
from users.DAO import UsersDAO
from fastapi import HTTPException, status
from users.auth import get_password_hash, auth_user, create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags = ["Auth"]
)

@router.post("/register")
async def register_user(response: Response, data: SUser):
    if await UsersDAO.find_existing(data.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with this username already exist")
    hashed_password = get_password_hash(data.password)
    id = await UsersDAO.insert_user(data.name, hashed_password)
    access_token = create_access_token({"sub":str(id)})
    response.set_cookie("todo_at", access_token)

@router.post("/login")
async def login(response: Response, data: SUser):
    user = await auth_user(data.name, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    access_token = create_access_token({"sub":str(user.id)})
    response.set_cookie("todo_at",
                        access_token,
                        httponly=True
                        )

@router.get("/me/")
async def get_me(user_data: str = Depends(get_current_user)):
    return user_data

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="todo_at")
    return {'message': 'Пользователь успешно вышел из системы'}