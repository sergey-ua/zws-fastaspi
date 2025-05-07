```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Optional

Base = declarative_base()

class UrlModel(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    short_id = Column(String, nullable=False, unique=True)
    is_blocked = Column(Boolean, default=False)

class UrlSchema(BaseModel):
    original_url: str
    short_id: str
    is_blocked: bool

    class Config:
        orm_mode = True

class UrlModelService:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    def create(self, url_schema: UrlSchema):
        try:
            session = self.Session()
            url_model = UrlModel(**url_schema.dict())
            session.add(url_model)
            session.commit()
            session.close()
            return url_model
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to create UrlModel: {str(e)}")

    def read(self, id: int) -> Optional[UrlModel]:
        try:
            session = self.Session()
            url_model = session.query(UrlModel).filter(UrlModel.id == id).first()
            session.close()
            return url_model
        except Exception as e:
            raise Exception(f"Failed to read UrlModel: {str(e)}")

    def update(self, id: int, url_schema: UrlSchema):
        try:
            session = self.Session()
            url_model = session.query(UrlModel).filter(UrlModel.id == id).first()
            if url_model is None:
                raise Exception("UrlModel not found")
            url_model.original_url = url_schema.original_url
            url_model.short_id = url_schema.short_id
            url_model.is_blocked = url_schema.is_blocked
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to update UrlModel: {str(e)}")

    def delete(self, id: int):
        try:
            session = self.Session()
            url_model = session.query(UrlModel).filter(UrlModel.id == id).first()
            if url_model is None:
                raise Exception("UrlModel not found")
            session.delete(url_model)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            raise Exception(f"Failed to delete UrlModel: {str(e)}")

    def validate_url_schema(self, url_schema: UrlSchema):
        try:
            UrlSchema(**url_schema.dict())
        except ValidationError as e:
            raise Exception(f"Invalid UrlSchema: {str(e)}")

def main():
    engine = create_engine('sqlite:///urls.db')
    Base.metadata.create_all(engine)
    url_model_service = UrlModelService(engine)
    url_schema = UrlSchema(original_url="https://example.com", short_id="example", is_blocked=False)
    url_model_service.validate_url_schema(url_schema)
    url_model_service.create(url_schema)
    read_url_model = url_model_service.read(1)
    print(read_url_model.original_url)
    updated_url_schema = UrlSchema(original_url="https://updated-example.com", short_id="updated-example", is_blocked=False)
    url_model_service.update(1, updated_url_schema)
    url_model_service.delete(1)

if __name__ == "__main__":
    main()
```