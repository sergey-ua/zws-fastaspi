package zws.database.models

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ValidationError
from base64 import b64encode
from typing import Optional
from zws.database.repositories import DatabaseRepository
from zws.services import Service

Base = declarative_base()

class ShortenedUrl(BaseModel):
    code: str

class Short(Base):
    __tablename__ = 'short'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)

    @staticmethod
    def parse(data: str, db_repository: DatabaseRepository, service: Service) -> str:
        if not isinstance(data, str):
            raise TypeError('Input data must be a string')
        try:
            shortened_url = ShortenedUrl.parse_obj({'code': data})
            db_repository.save_shortened_url(shortened_url.code)
            service.process_shortened_url(shortened_url.code)
            return shortened_url.code
        except ValidationError as e:
            raise ValueError('Invalid input data') from e

    @staticmethod
    def toBase64(code: str) -> str:
        if not isinstance(code, str):
            raise TypeError('Input code must be a string')
        try:
            return b64encode(code.encode()).decode()
        except Exception as e:
            raise Exception('Failed to encode to Base64') from e

    def __init__(self, code: str, db_repository: DatabaseRepository, service: Service):
        self.code = code
        db_repository.save_shortened_url(code)
        service.process_shortened_url(code)