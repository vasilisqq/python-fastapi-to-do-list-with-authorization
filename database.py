from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import settings

engine = create_async_engine(settings.DB_URL.get_secret_value())
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit= False
)

class Base(DeclarativeBase):
    ...