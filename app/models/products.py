from sqlalchemy import Column, DateTime, Integer, String, func,Float
from app.database import Base


class ProductTable(Base):
    __tablename__="products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    description = Column(String(100), nullable=True)
    price = Column(Float,nullable=False)
    stock = Column(Integer,nullable=False)
    category = Column(String(50),nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)