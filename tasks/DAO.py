from database import async_session_maker
from sqlalchemy import select
from tasks.model import Tasks

class DAO:
    @classmethod
    async def get_all_tasks_from_user(cls, user_id: int):
        async with async_session_maker() as session:
            query = select(Tasks).where(Tasks.user_id==user_id)
            result = await session.execute(query)
            return [Tasks.from_orm(user) for user in result]