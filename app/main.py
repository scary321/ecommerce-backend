from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session ,status
from app.schemas import UserResponse
from app.schemas import UserCreate
from app.database import get_db

app = FastAPI()

@app.get("/")
def root():
    return {"message": "database connection successful!"}


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user: UserCreate,db: Session = Depends(get_db)):

    return db_user