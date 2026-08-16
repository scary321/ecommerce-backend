from app.database import get_db
from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.auth import get_current_user,require_admin
from app.models.payment import PaymentTable
from app.schemas.payment import PaymentCreate,PaymentResponse,PaymentStatusUpdate,RazorpayOrderResponse
from app.models.orders import OrderTable
from app.utils.razorpay import razorpay_client
from app.config import settings

payment_router = APIRouter()

@payment_router.post("/payments",status_code=status.HTTP_201_CREATED,response_model=PaymentResponse)
def create_payment(payment:PaymentCreate,current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    
    order = db.query(OrderTable).filter(OrderTable.id == payment.order_id).first()
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no order exist")
    
    if order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="access denied")
    
    if order.status == "cancelled":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="order is cancelled")
    
    existing_payments =db.query(PaymentTable).filter(PaymentTable.order_id == payment.order_id).first()
    
    if existing_payments:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="order is already paid")
    
    new_payment=PaymentTable(
        order_id = order.id,
        amount = order.total,
        payment_method = payment.payment_method,
        status="pending",
        transaction_id=None
    )
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment

@payment_router.patch("/admin/payments/{id}/status",response_model=PaymentResponse)
def update_payment_status(id:int,status_update: PaymentStatusUpdate,current_user=Depends(require_admin),db:Session = Depends(get_db)):
    
    payment = db.query(PaymentTable).filter(PaymentTable.id == id).first()
    
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="payment not found")
    
    status_payment=["pending","successful","failed","refunded"]
        
    if status_update.status not in status_payment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid status")
    
    if payment.status == "pending":
        allowed_update = ["successful","failed"]
            
    if payment.status == "successful":
        allowed_update = ["refunded"]
        
    if payment.status == "refunded":
        allowed_update = []
    
    if payment.status == "failed":
        allowed_update = []
        
    if status_update.status not in allowed_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid status transition")
        
    payment.status = status_update.status
    
    order=db.query(OrderTable).filter(OrderTable.id == payment.order_id).first()
    
    if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
    
    if payment.status == "successful":
        order.status="processing"
    
    if payment.status == "refunded":
        order.status="cancelled"    
        
    db.commit()
    db.refresh(payment)
    return payment

@payment_router.post("/payments/{order_id}/create",status_code=status.HTTP_201_CREATED,response_model=RazorpayOrderResponse)
def create_payment(order_id:int,current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    
    order =db.query(OrderTable).filter(order_id == OrderTable.id).first()
    
    if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
        
    if order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="access denied")
    
    if order.status == "cancelled":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="order is cancelled")
    
    amount_paise = int(order.total * 100)
    
    razorpay_order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })
    
    return RazorpayOrderResponse(
        id=razorpay_order["id"],
        amount=razorpay_order["amount"],
        currency=razorpay_order["currency"],
        razorpay_key_id=settings.RAZORPAY_KEY_ID
    )