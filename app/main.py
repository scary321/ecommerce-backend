from app.routers.users import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)