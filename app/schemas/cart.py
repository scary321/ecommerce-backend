from pydantic import BaseModel, ConfigDict

class CartItemCreate(BaseModel):
    product_id:int
    quantity:int
    
class CartItemUpdate(BaseModel):
    quantity:int
    
class CartItemResponse(BaseModel):
    id:int
    product_id:int
    quantity:int
    
    model_config=ConfigDict(from_attributes=True)