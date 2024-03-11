from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from config import settings
from db import engine, session  
from models.links import Links, LinksSchema
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shortuuid  
from fastapi.security import OAuth2PasswordBearer
from models.base import Base
from models.users import User, UserSchema, UserAccountSchema
from models.token import Token, TokenData, create_access_token
from services import create_user, get_user
from datetime import date, timedelta
from starlette.responses import RedirectResponse
import jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    return app

app = start_application()

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
    from sqlalchemy.orm import Session

    uvicorn.run(app, host="127.0.0.1", port=8000)

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
    session.add(db_link)  # Use 'session' directly
    session.commit()
    session.refresh(db_link)

    # Return the generated short URL
    return {"short_url": short_url}

@app.get("/read")
def read_links():
    links = session.query(Links).all()  # Use 'session' directly
    return {"links": [{"short_url": link.short_url, "long_url": link.long_url} for link in links]}

@app.post("/register", response_model=UserSchema)
def register_user(payload: UserAccountSchema):
    payload.hashed_password = User.hash_password(payload.hashed_password)

    return create_user(user=payload)

@app.post("/login")
async def login(payload: UserAccountSchema):
    try:
        user: User = get_user(email=payload.email)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User Credentials"
        )

    is_validated: bool = user.validate_password(payload.hashed_password)

    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User Credentials"
        )
    access_token_expires = timedelta(minutes=120)
    access_token = create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/sendit")
async def redirect_to_external_url(url: str = Query(...)):
    link = session.query(Links).filter(Links.short_url == url).first()
    return RedirectResponse(link.long_url)
