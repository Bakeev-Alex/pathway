import uuid

from sqlalchemy import Column, String, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    """Модель пользователя."""
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String(100), )
    last_name = Column(String(100), )
    tg_id = Column(String(50), nullable=False)

    points = relationship("CoordinatePoint", back_populates="user", cascade="all, delete-orphan")
