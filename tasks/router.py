from fastapi import APIRouter, Depends, Request, Response
from tasks.DAO import DAO
from users.auth.auth import validate_tokens


router = APIRouter(
    prefix="/tasks",
    tags = ["tasks"]
)

@router.get("/me/")
async def get_all_tasks(user_id: str = Depends(validate_tokens)):
    return await DAO.get_all_tasks_from_user(user_id=int(user_id))


@router.get("/me/add")
async def create_new_task(
    title: str,
    user_id: str = Depends(validate_tokens),
    description : str|None = None,
):
    await DAO.create_new_task(
        int(user_id),
        title,
        description,
    )