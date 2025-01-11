from fastapi import APIRouter, Depends
from users.auth.auth import get_all_tasks
from jose import jwt
from config import settings
from tasks.schemas import STask


router = APIRouter(
    prefix="/tasks",
    tags = ["tasks"]
)

@router.get("/me/")
async def get_me(tasks: list[STask] = Depends(get_all_tasks)):
    return tasks