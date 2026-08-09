from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status,Depends
from app.database import get_db
from sqlalchemy.orm import Session 
from jose import JWTError,jwt
from app import models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    
    payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    
    user_id=payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    user = db.query(models.UsersTable).filter(models.UsersTable.id == user_id).first()
    
    if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
    return user

def require_admin(current_user=Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return current_user