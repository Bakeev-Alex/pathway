import uuid

from sqlalchemy import Column, String, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class CoordinatePoint(Base):
    """
    Координаты и данные точки.

    Arguments:
        id (UUID): Id координат
        latitude (str): Широта
        longitude (str): Долгота
        message (str): Сообщение
        user_id (str): Id пользователя
        image_id (UUID): Ids изображений
    """
    __tablename__ = "coordinate_points"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    latitude = Column(String(50))
    longitude = Column(String(50))
    message = Column(Text)
    user_id = Column(String(150), ForeignKey("users.tg_id", ondelete='CASCADE'), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey("image_points.id", ondelete='CASCADE'))

    user = relationship('User', back_populates='points')
    image = relationship('ImagePoint', back_populates='points')