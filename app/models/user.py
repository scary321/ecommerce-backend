from sqlalchemy import Column, DateTime, Integer, String, func
from app.database import Base


class UsersTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    role = Column(String(15),default="user")
