from app.database import get_db
from fastapi import APIRouter , Depends, status ,HTTPException
from sqlalchemy.orm import Session 
from app.auth import get_current_user
from app.models.payment import PaymentTable
from app.schemas.payment import PaymentCreate,PaymentResponse
from app.models.orders import OrderTable

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