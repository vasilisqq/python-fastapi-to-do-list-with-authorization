from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database import Base

class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default="n")