from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from config.core import Setting
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

engine = create_engine(url=Setting.DB_CONNECTION_STR, echo=False) # echo = show-sql
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # Index
    created_at = Column(DateTime, server_default=func.now()) # created record server time at
    updated_at = Column(DateTime, onupdate=func.now()) # updated record server time at

def get_session() -> Generator:
  try:
    session = Session()
    yield session
  finally:
    session.close()
    