from pydantic import BaseModel, ConfigDict

class STask(BaseModel):
    id: int
    user_id: int
    title: str
    description : str|None = None
    completed: bool
    model_config = ConfigDict(from_attributes=True)