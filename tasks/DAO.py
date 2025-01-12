from database import async_session_maker
from sqlalchemy import select, insert, delete, and_
from tasks.model import Tasks
from tasks.schemas import STask

class DAO:
    @classmethod
    async def get_all_tasks_from_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Tasks).where(Tasks.user_id==user_id)
            result = await session.execute(query)
            tasks = result.scalars().all()
            return [STask.from_orm(task) for task in tasks]
    @classmethod
    async def create_new_task(
        cls,
        user_id,
        title: str,
        description : str|None = None
    ):
        async with async_session_maker() as session:
            query = insert(Tasks).values(
                user_id = user_id,
                title=title,
                description=description
            )
            await session.execute(query)
            await session.commit()
    @classmethod
    async def delete_task(cls, user_id: int, task_id: int):
        async with async_session_maker() as session:
            query = delete(Tasks).where(and_(
                Tasks.user_id == user_id, Tasks.id == task_id))
            await session.execute(query)
            await session.commit()