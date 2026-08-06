from fastapi import FastAPI , Depends,status
from sqlalchemy.orm import Session 
from app.schemas import UserResponse
from app.schemas import UserCreate
from app.database import get_db
from app.utils import hash_password
from app.models import UsersTable

app = FastAPI()

@app.get("/")
def root():
    return {"message": "database connection successful!"}


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    new_user = UsersTable(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user