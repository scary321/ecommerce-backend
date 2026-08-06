from fastapi import FastAPI
from app.schemas import UserResponse
app = FastAPI()

@app.get("/")
def root():
    return {"message": "database connection successful!"}


