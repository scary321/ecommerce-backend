from fastapi import FastAPI , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.schemas import UserResponse ,UserCreate,UserLogin,LoginResponse,UserUpdate
from app.database import get_db
from app.utils import hash_password,verify_password,create_access_token
from app.models import UsersTable
from app import models
from jose import JWTError,jwt
from .config import settings
from app.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import update


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
def login_user(user_credential: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    
    user = db.query(models.UsersTable).filter(
    models.UsersTable.email == user_credential.username
).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not verify_password(user_credential.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token=create_access_token(data={"user_id":user.id})
    return{"access_token":access_token,"token_type":"bearer"}

@app.get("/users/{id}",response_model=UserResponse)
def get_user(id:int, current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    user = db.query(models.UsersTable).filter(models.UsersTable.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if (current_user.id != id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied")
    
    return user

@app.patch("/users/{id}",response_model=UserResponse)
def update_user(id:int,user_update: UserUpdate, current_user=Depends(get_current_user),db:Session = Depends(get_db)):
    if (current_user.id != id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied")
    user = db.query(models.UsersTable).filter(models.UsersTable.id == id).first()    
    
    if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    if user_update.email:
        user.email = user_update.email  
    if user_update.password:
        user.password_hash =hash_password(user_update.password)
        
    db.commit()
    db.refresh(user)
    
    return user