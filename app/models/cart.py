from sqlalchemy import Column, DateTime, Integer, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CartTable(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),unique=True,nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("UsersTable",back_populates="cart")

    cart_items = relationship("CartItemTable",back_populates="cart",cascade="all, delete-orphan")


class CartItemTable(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer,ForeignKey("carts.id", ondelete="CASCADE"),nullable=False)
    product_id = Column(Integer,ForeignKey("products.id", ondelete="CASCADE"),nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    cart = relationship("CartTable",back_populates="cart_items")

    product = relationship("ProductTable",back_populates="cart_items")