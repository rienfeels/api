from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config import settings
from db import engine, session
from models.links import Links, LinksSchema
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shortuuid  
from models.base import Base
from models.users import User, UserSchema, UserAccountSchema
from services import create_user


def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION);
    create_tables()
    return app

app = start_application()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.post("/create")
def create_link(link: LinksSchema):
    # Generate a short URL using shortuuid
    short_url = shortuuid.uuid()[:8]  # Adjust the length as needed

    # Create a new Links instance
    db_link = Links(
        title=link.title,
        long_url=link.long_url,
        short_url=short_url,
        user_id=link.user_id
    )

    # Add to the database
    db.add(db_link)
    db.commit()
    db.refresh(db_link)

    # Return the generated short URL
    return {"short_url": short_url}

@app.get("/read")
def read_links():
    links = db.query(Links).all()
    return {"links": [{"short_url": link.short_url, "long_url": link.long_url} for link in links]}

@app.post("/register", response_model=UserSchema)
def register_user(payload: UserAccountSchema):
    payload.hashed_password = User.hash_password(payload.hashed_password)

    return create_user(user=payload)


origins = [
    "http://localhost:*",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
