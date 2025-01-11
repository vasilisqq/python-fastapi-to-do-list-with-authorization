from pydantic import BaseModel

class STask(BaseModel):
    id: int
    user_id: int
    title: str
    description : str|None = None
    completed: bool
    class Config:
        orm_mode = True