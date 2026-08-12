from pydantic import BaseModel, ConfigDict
from datetime import datetime

class OrderItemResponse(BaseModel):
    id:int
    product_id:int
    quantity:int
    price:float
    
    model_config = ConfigDict(from_attributes=True)
    
class OrderResponse(BaseModel):
    id:int
    total:float
    status:str
    created_at:datetime
    items:list[OrderItemResponse]
    
    model_config = ConfigDict(from_attributes=True)