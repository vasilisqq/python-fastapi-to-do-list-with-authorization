from fastapi import FastAPI
from config import settings
from users.router import router as users_router
from tasks.router import router as tasks_router


app = FastAPI()
app.include_router(users_router)
app.include_router(tasks_router)
