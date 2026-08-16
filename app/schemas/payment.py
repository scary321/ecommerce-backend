from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class PaymentCreate(BaseModel):
    order_id:int
    payment_method:str
    
class PaymentResponse(BaseModel):
    id:int
    order_id:int
    amount:Decimal
    payment_method:str
    status:str
    transaction_id:str|None=None
    
    model_config=ConfigDict(from_attributes=True)
    
class PaymentStatusUpdate(BaseModel):
    status:str
    
class RazorpayOrderResponse(BaseModel):
    razorpay_order_id: str
    amount: int
    currency: str
    razorpay_key_id: str

    model_config = ConfigDict(from_attributes=True)
    
class RazorpayPaymentVerification(BaseModel):
    
    razorpay_order_id:str
    razorpay_payment_id:str
    razorpay_signature:str