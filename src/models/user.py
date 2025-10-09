import uuid

from sqlalchemy import Column, String, UUID, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    """
    Модель пользователя.

    Arguments:
        tg_id (str): ID пользователя в телеграмм
        first_name (str): Имя
        last_name (str): Фамилия
        is_active (bool): Активность
        username (str): Имя пользователя в телеграмм
    """
    __tablename__ = "users"
    tg_id = Column(String(150), primary_key=True, index=True)
    first_name = Column(String(100), )
    last_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    username = Column(String(100), nullable=True)

    points = relationship("CoordinatePoint", back_populates="user", cascade="all, delete-orphan")
