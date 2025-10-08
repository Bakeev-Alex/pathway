import uuid

from sqlalchemy import Column, String, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    """Модель пользователя."""
    # todo: Для этой модели нужно создать простую регистрацию, которая будет привязываться к tg_id и в случае
    #  Не корректного поведения пользователя, блокировать его.

    # todo: Так же во всех методах нужно проверять, что пользователь зарегистрирован и просить его пройти регистрацию
    #  Только после этого, пользователь может оставить свои координаты
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # todo: Мне кажется эти поля избыточные, можно просто сохранять tg_id и имя, которые есть в tg.
    first_name = Column(String(100), )
    last_name = Column(String(100), )
    tg_id = Column(String(50), nullable=False)

    points = relationship("CoordinatePoint", back_populates="user", cascade="all, delete-orphan")
