from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,)
    last_name = Column(String)
    age = Column(Integer)