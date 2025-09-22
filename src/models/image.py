import uuid

from sqlalchemy import Column, Integer, String, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ImagePoint(Base):
    __tablename__ = 'image_points'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    size = Column(String)
    file_path = Column(String(255), nullable=False)

    points = relationship("CoordinatePoint", back_populates="image")