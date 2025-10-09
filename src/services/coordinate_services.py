from typing import Any

from src.models import CoordinatePoint
from src.database import async_session


class CoordinatePointService:

    @classmethod
    async def create_coordinate(cls, data: dict[str, Any]):
        """Сохранение координат пользователя без изображений."""
        async with async_session() as session:
            point = CoordinatePoint(**data)
            session.add(point)
            await session.commit()
