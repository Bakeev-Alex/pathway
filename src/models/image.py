import uuid

from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship

from src.database import Base


class ImagePoint(Base):
    """
    Модель изображений.

    Arguments:
        id (UUID): Id изображения
        size (UUID): Размер изображения
        file_path (UUID): Путь к файлу на облаке.
    """
    __tablename__ = 'image_points'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    size = Column(String)
    file_path = Column(String(255), nullable=False)

    points = relationship("CoordinatePoint", back_populates="image")