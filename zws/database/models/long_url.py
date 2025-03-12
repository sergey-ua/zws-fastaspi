package zws.database.models

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from fastapi import FastAPI, RedirectResponse
from typing import Optional
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Short(Base):
    __tablename__ = "short"
    id = Column(Integer, primary_key=True)

class LongUrl(Base):
    __tablename__ = "long_url"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    short_id = Column(Integer, ForeignKey("short.id"))
    short = relationship("Short", backref="long_urls")

    def redirect(self):
        return RedirectResponse(url=self.url)

class LongUrlPydantic(BaseModel):
    url: str

    class Config:
        orm_mode = True

    def to_database(self):
        return LongUrl(url=self.url)

    @staticmethod
    def from_database(long_url: LongUrl):
        return LongUrlPydantic(url=long_url.url)

    def redirect(self, long_url: LongUrl):
        return RedirectResponse(url=long_url.url)

class ShortUrlPydantic(BaseModel):
    short: str

    class Config:
        orm_mode = True

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

@app.get("/redirect/{url_id}")
def read_redirect(url_id: int):
    long_url = session.query(LongUrl).filter(LongUrl.id == url_id).first()
    if long_url:
        return long_url.redirect()
    else:
        return {"error": "URL not found"}

@app.post("/create")
def create_long_url(long_url_pydantic: LongUrlPydantic):
    long_url = long_url_pydantic.to_database()
    session.add(long_url)
    session.commit()
    return {"id": long_url.id}

@app.get("/get/{url_id}")
def get_long_url(url_id: int):
    long_url = session.query(LongUrl).filter(LongUrl.id == url_id).first()
    if long_url:
        return LongUrlPydantic.from_database(long_url)
    else:
        return {"error": "URL not found"}