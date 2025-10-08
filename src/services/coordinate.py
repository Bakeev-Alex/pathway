from typing import Any

from src.models import CoordinatePoint
from src.database import async_session


class CoordinatePointService:

    @classmethod
    async def create_coordinate(cls, data: dict[str, Any]):
        """Сохранение координат пользователя без изображений."""
        async with async_session() as session:
            # point = CoordinatePoint(
            #     latitude='57.792093',
            #     longitude='28.209667',
            #     message='text_message',
            #     user_id='d4eebf98-2d1a-46a4-8f3c-40eb247cbbcc'
            # )
            point = CoordinatePoint(**data)
            session.add(point)
            await session.commit()

    @classmethod
    async def create_coordinate_with_image(cls, data: dict[str, Any]):
        """Сохранение координат пользователя c изображением."""
        # Todo: Скорее всего, нужно будет сделать только один метод,
        #  который будет сохранять по флагу с изображениями или без.
        #  А отдельный метод, будет сохранять в облако изображения и сохранять путь до файла.
        ...
