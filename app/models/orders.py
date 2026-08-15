from sqlalchemy import Column, DateTime, Integer, String, func,Numeric,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OrderTable(Base):
    __tablename__ = "orders"
    
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    total=Column(Numeric,nullable=False)
    status=Column(String,nullable=False,default="pending")
    created_at=Column(DateTime, default=func.now(), nullable=False)
    
    user = relationship("UsersTable",back_populates="orders")
    
    items = relationship("OrderItemTable",back_populates="order",cascade="all, delete-orphan")
    
    payment = relationship("PaymentTable",back_populates="order",uselist=False,cascade="all, delete-orphan")
    
class OrderItemTable(Base):
    __tablename__ = "order_items"
    
    id=Column(Integer,primary_key=True)
    order_id=Column(Integer,ForeignKey("orders.id", ondelete="CASCADE"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id", ondelete="CASCADE"),nullable=False)
    quantity=Column(Integer,nullable=False)
    price=Column(Numeric,nullable=False)
    
    order = relationship("OrderTable",back_populates="items")
    
    product = relationship("ProductTable",back_populates="order_item")