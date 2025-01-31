from datetime import datetime

# from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from users.models import User
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): pass


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey(User.id))
    recipient_id = Column(Integer, ForeignKey(User.id))
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship(User, foreign_keys=[sender_id])
    recipient = relationship(User, foreign_keys=[recipient_id])
