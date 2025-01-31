from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
# from db import Base


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    name = Column(String, index=True)
    age = Column(Integer, nullable=True)
    password = Column(String(length=1024), nullable=False)
