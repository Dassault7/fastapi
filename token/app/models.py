"""
token: Database models for the token app
"""
from sqlalchemy import Column, Integer, String, Enum as SQLEnum

from app.db import Base
from app.schemas import UserLevel


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    level = Column(SQLEnum(UserLevel))
    hashed_password = Column(String)
