from fastapi import FastAPI , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.schemas import UserResponse ,UserCreate,UserLogin,LoginResponse
from app.database import get_db
from app.utils import hash_password,verify_password,create_access_token
from app.models import UsersTable
from app import models
from jose import JWTError,jwt
from .config import settings


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

@app.post("/login",response_model=LoginResponse)
def login_user(user_credential:UserLogin,db:Session = Depends(get_db)):
    
    user = db.query(models.UsersTable).filter(models.UsersTable.email == user_credential.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not verify_password(user_credential.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token=create_access_token(data={"user_id":user.id})
    return{"access_token":access_token,"token_type":"bearer"}