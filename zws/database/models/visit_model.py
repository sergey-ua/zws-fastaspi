package zws.database.models;

import sqlalchemy.Column;
import sqlalchemy.String;
import sqlalchemy.Integer;
import sqlalchemy.DateTime;
import sqlalchemy.ForeignKey;
import sqlalchemy.ext.declarative.declarative_base;

Base = declarative_base();

public class VisitModel(Base):
    __tablename__ = "visits";

    id = Column(Integer, primary_key=True, autoincrement=True);
    url_short_base64 = Column(String, ForeignKey("urls.short_base64"), nullable=False);
    timestamp = Column(DateTime, default=datetime.utcnow);