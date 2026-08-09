from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    
    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    email: EmailStr
    password:str
    
class LoginResponse(BaseModel):
    access_token:str
    token_type:str
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password:Optional[str]
    
class AdminRoleUpdate(BaseModel):
    role:str
    