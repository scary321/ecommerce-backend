from sqlalchemy import Column,Integer, String,Float,ForeignKey,Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class PaymentTable(Base):
    __tablename__="payments"
    
    id = Column(Integer,primary_key=True)
    order_id = Column(Integer,ForeignKey("orders.id", ondelete="CASCADE"),nullable=False,unique=True)
    amount = Column(Numeric,nullable=False)
    payment_method = Column(String,nullable=False)
    status=Column(String,nullable=False,default="pending")
    transaction_id = Column(String,unique=True,nullable=True)
    razorpay_order_id = Column(String,unique=True,nullable=True)
    
    order = relationship("OrderTable",back_populates="payment")