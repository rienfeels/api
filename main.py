from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config import Settings
from db import SessionLocal 
from models.links import Links, LinksSchema
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shortuuid  # Import the shortuuid library

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create")
def create_link(link: LinksSchema, db: Session = Depends(get_db)):
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
def read_links(db: Session = Depends(get_db)):
    links = db.query(Links).all()
    return {"links": [{"short_url": link.short_url, "long_url": link.long_url} for link in links]}


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
