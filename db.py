from sqlalchemy import create_engine
# from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()