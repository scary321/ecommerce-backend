from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ProductCreate(BaseModel):
    name:str
    description:str
    price:float
    stock:int
    category:str
    
class ProductResponse(BaseModel):
    id:int
    name:str
    price:float
    description:str
    stock:int
    category:str
    created_at:datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class ProductUpdate(BaseModel):
    name:str|None=None
    description:str|None=None
    price:float|None=None
    stock:int|None=None
    category:str|None=None
    