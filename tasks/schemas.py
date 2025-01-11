from pydantic import BaseModel

class STask(BaseModel):
    id: int
    user_id: int
    title: str
    description : str|None = None
    completed: bool
    class Config:
        from_attributes = True