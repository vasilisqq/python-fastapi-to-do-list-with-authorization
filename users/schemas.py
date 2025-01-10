from pydantic import BaseModel

class SUser(BaseModel):
    name: str
    password: str
