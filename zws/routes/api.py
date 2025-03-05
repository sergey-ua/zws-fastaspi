```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, DatabaseError
from typing import Optional
from uuid import uuid4
from logging import getLogger, StreamHandler, Formatter
from blocked_hostnames_service import BlockedHostnamesService
from url_service import UrlService

app = FastAPI()

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///urls.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the URL model
class Url(Base):
    __tablename__ = "urls"
    id = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)
    blocked = Column(Integer, nullable=False, default=0)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Define the request model
class UrlRequest(BaseModel):
    url: str

    @validator("url")
    def validate_url(cls, v):
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("Invalid URL")
        return v

# Define the response model
class UrlResponse(BaseModel):
    shortened_url: str

# Initialize the BlockedHostnamesService and UrlService
blocked_hostnames_service = BlockedHostnamesService()
url_service = UrlService()

# Initialize logging
logger = getLogger(__name__)
logger.setLevel("INFO")
handler = StreamHandler()
handler.setFormatter(Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

# POST endpoint to shorten a URL
@app.post("/", response_model=UrlResponse)
def shorten_url(url_request: UrlRequest):
    try:
        # Check if the URL is blocked
        if blocked_hostnames_service.is_blocked(url_request.url):
            logger.warning("URL is blocked: %s", url_request.url)
            raise HTTPException(status_code=400, detail="URL is blocked")

        # Generate a unique short ID
        short_id = str(uuid4())[:6]

        # Store the URL mapping in the database
        db = SessionLocal()
        url = Url(id=short_id, original_url=url_request.url)
        try:
            db.add(url)
            db.commit()
        except IntegrityError:
            db.rollback()
            logger.error("Failed to store URL mapping: %s", url_request.url)
            raise HTTPException(status_code=500, detail="Failed to store URL mapping")
        except DatabaseError as e:
            db.rollback()
            logger.error("Database error: %s", str(e))
            raise HTTPException(status_code=500, detail="Database error: " + str(e))

        # Return the shortened URL
        logger.info("URL shortened: %s -> %s", url_request.url, f"http://localhost:8000/{short_id}")
        return {"shortened_url": f"http://localhost:8000/{short_id}"}
    except Exception as e:
        logger.error("Internal server error: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

# GET endpoint to retrieve the original URL
@app.get("/{short_id}")
def get_original_url(short_id: str):
    try:
        # Retrieve the original URL from the database
        db = SessionLocal()
        url = db.query(Url).filter(Url.id == short_id).first()
        if not url:
            logger.warning("URL not found: %s", short_id)
            raise HTTPException(status_code=404, detail="URL not found")

        # Check if the URL is blocked
        if url.blocked:
            logger.warning("URL is blocked: %s", url.original_url)
            raise HTTPException(status_code=400, detail="URL is blocked")

        # Return the original URL
        logger.info("Original URL retrieved: %s -> %s", short_id, url.original_url)
        return {"original_url": url.original_url}
    except Exception as e:
        logger.error("Internal server error: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
```