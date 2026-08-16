from app.database import get_db
from fastapi import APIRouter , Depends, status ,HTTPException,Request
from sqlalchemy.orm import Session 
from app.auth import get_current_user,require_admin
from app.models.payment import PaymentTable
from app.schemas.payment import PaymentCreate,PaymentResponse,PaymentStatusUpdate,RazorpayOrderResponse,RazorpayPaymentVerification
from app.models.orders import OrderTable
from app.utils.razorpay import razorpay_client
from app.config import settings
import razorpay
import json


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
def create_razor_payment(order_id:int,current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    
    order =db.query(OrderTable).filter(OrderTable.id == order_id).first()
    
    if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
        
    if order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="access denied")
    
    if order.status == "cancelled":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="order is cancelled")
    
    existing_payment = db.query(PaymentTable).filter(PaymentTable.order_id == order.id).first()

    if existing_payment:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Payment already exists for this order")
    
    amount_paise = int(order.total * 100)
    
    razorpay_order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })
    
    new_payment=PaymentTable(
            order_id = order.id,
            amount = order.total,
            payment_method = "razor_pay",
            status="pending",
            transaction_id=None,
            razorpay_order_id=razorpay_order["id"]
        )
    
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    
    return RazorpayOrderResponse(
    razorpay_order_id=razorpay_order["id"],
    amount=razorpay_order["amount"],
    currency=razorpay_order["currency"],
    razorpay_key_id=settings.RAZORPAY_KEY_ID
)
    
@payment_router.post("/payments/verify",response_model=PaymentResponse)
def razor_pay_verification(verify:RazorpayPaymentVerification,current_user=Depends(get_current_user),db: Session = Depends(get_db)):
    
    payment = db.query(PaymentTable).filter(PaymentTable.razorpay_order_id== verify.razorpay_order_id).first()
    
    if not payment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="payment not found")
    
    order = db.query(OrderTable).filter(OrderTable.id == payment.order_id).first()
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")
    

    if order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="access denied")        
    
    try:
        razorpay_client.utility.verify_payment_signature({
        "razorpay_order_id": verify.razorpay_order_id,
        "razorpay_payment_id": verify.razorpay_payment_id,
        "razorpay_signature": verify.razorpay_signature
    })

    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid payment signature"
    )
    payment.status = "successful"
    payment.transaction_id = verify.razorpay_payment_id

    order.status = "processing"

    db.commit()
    db.refresh(payment)

    return payment    


@payment_router.post("/payments/webhook",status_code=status.HTTP_200_OK)
async def razor_pay_verification_webhook(request: Request,db: Session = Depends(get_db)
):
    body = await request.body()

    signature = request.headers.get("X-Razorpay-Signature")

    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Razorpay signature missing"
        )

    try:
        razorpay_client.utility.verify_webhook_signature(
            body.decode("utf-8"),
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature"
        )

    payload = json.loads(body)

    event = payload.get("event")

    if event == "payment.captured":
        payment_entity = payload["payload"]["payment"]["entity"]

        razorpay_order_id = payment_entity["order_id"]
        razorpay_payment_id = payment_entity["id"]

        payment = db.query(PaymentTable).filter(
            PaymentTable.razorpay_order_id == razorpay_order_id
        ).first()

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )

        if payment.status == "successful":
            return {"message": "Successful payment cannot be marked as failed"}

        payment.status = "failed"
        payment.transaction_id = razorpay_payment_id

        db.commit()

    return {"message": "Webhook processed"}