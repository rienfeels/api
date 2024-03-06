from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column
from pydantic import BaseModel
from models.base import Base
from models.users import User

class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    long_url = Column(String)
    short_url = Column(String)
    user_id = mapped_column(ForeignKey("users.id"))

class LinksSchema(BaseModel):
    title: str
    long_url: str
    short_url: str
    user_id: int

    class Config:
        populate_by_name = True
