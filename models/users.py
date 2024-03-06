from sqlalchemy import Column, Integer, String, UniqueConstraint
from pydantic import BaseModel, Field

from config import settings
from models.base import Base

import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    hashed_password = Column(String)

    UniqueConstraint("email", name="uq_user_email")

    def __repr__(self):
        return f"<User {self.email!r}>"
    
    @staticmethod
    def hash_password(password) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def validate_password(self, pwd):
        return bcrypt.checkpw(password=pwd.encode(), hashed_password=self.hashed_password.encode())
    
class UserBaseSchema(BaseModel):
    email: str

class UserSchema(UserBaseSchema):
    id: int

    class Config:
        populate_by_name = True

class UserAccountSchema(UserBaseSchema):
    hashed_password: str = Field(alias="password")