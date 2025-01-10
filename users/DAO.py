from users.model import Users
from database import async_session_maker
from sqlalchemy import select, insert
from users.schemas import SUser
class UsersDAO():
    @classmethod
    async def find_existing(cls, name:str):
        async with async_session_maker() as session:
            query = select(Users).where(Users.name==name)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    @classmethod
    async def insert_user(cls, name: str, hashed_password:str):
        async with async_session_maker() as session:
            query = insert(Users).values(
                name=name,
                hashed_password=hashed_password
                )
            await session.execute(query)
            await session.commit()
