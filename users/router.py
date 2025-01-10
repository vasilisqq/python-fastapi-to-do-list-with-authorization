from fastapi import APIRouter
from users.schemas import SUser
from users.DAO import UsersDAO
from fastapi import HTTPException, status
from users.auth import get_password_hash

router = APIRouter(
    prefix="/auth",
    tags = ["Auth"]
)

@router.post("/register")
async def register_user(data: SUser):
    if await UsersDAO.find_existing(data.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with this username already exist")
    hashed_password = get_password_hash(data.password)
    await UsersDAO.insert_user(data.name, hashed_password)

