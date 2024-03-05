from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    long_url = Column(String)
    short_url = Column(String)
    user_id = Column(Integer)

class LinksSchema(BaseModel):
    title: str
    long_url: str
    short_url: str
    user_id: int

    class Config:
        populate_by_name = True
