from sqlalchemy import Column, Integer, String, UniqueConstraint
from pydantic import BaseModel, Field

from config import settings
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String)

    UniqueConstraint("email", name="uq_user_email")