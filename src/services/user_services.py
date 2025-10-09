from sqlalchemy import select, exists
from aiogram.types import Message

from src.models import User
from src.database import async_session


class UserService:
    model = User

    @classmethod
    async def check_user(cls, tg_id: int) -> bool:
        """
        Проверка присутствия пользователя в системе.

        Args:
            tg_id (int): tg_id для поиска пользователя.
        """
        async with async_session() as session:
            stmt = select(exists().where(cls.model.tg_id == str(tg_id)))
            result = await session.execute(stmt)
            exists_user = result.scalar()

        return exists_user

    @classmethod
    async def create_user_from_message(cls, message: Message) -> None:
        """
        Сохранение координат пользователя без изображений.

        Args:
            message (Message): Объект сообщения.
        """
        data = {
            'tg_id': f'{message.from_user.id}',
            'first_name': f'{message.from_user.first_name}',
            'last_name': message.from_user.last_name,
            'username': message.from_user.username,
        }

        async with async_session() as session:
            user = cls.model(**data)
            session.add(user)
            await session.commit()
        return
