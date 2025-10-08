from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, Message, ReplyKeyboardRemove

from src.services import coordinate_service
# import aiogram.utils.markdown as fmt

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

share_location_route = Router()

# todo: Так же нужно добавить отмену на каждый шаг процесса.


class ShareLocationState(StatesGroup):
    coordinates = State()
    comment = State()
    photo = State()


@share_location_route.message(Command('share_location'))
async def position_handler(message: Message, state: FSMContext):
    """Вступительное сообщение для получения координат по нажатию на кнопку."""
    # todo: Было бы классно проверять пользователя, что есть в системе и передавать id его, до сохранения данных.
    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Отправить координаты', request_location=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    # todo: Тут можно поймать ошибку, что координаты можно отправить из телефона только, надо ее обработать.

    await message.answer('Отправь координаты.', reply_markup=location_keyboard)

    await state.set_state(ShareLocationState.coordinates)


@share_location_route.message(F.content_type == ContentType.LOCATION, ShareLocationState.coordinates)
async def get_positions(message: Message, state: FSMContext):
    """Обработай и сохрани координаты позиции."""
    location = message.location
    await state.update_data(latitude=location.latitude, longitude=location.longitude)
    await message.answer(
        'Отправьте до 5 изображений и текст под сообщением (300 символов), для публикации на карте.',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(ShareLocationState.comment)


@share_location_route.message(ShareLocationState.comment)
async def get_comments_with_image(message: Message, state: FSMContext):
    """Получение и обработка текста с изображением."""
    # todo: В данной реализации, сообщение и изображение отправляется обратно.
    #  В дальнейшем они будут сохраняться и выводится на карту.

    data = await state.get_data()

    user_id = "d4eebf98-2d1a-46a4-8f3c-40eb247cbbcc"

    if message.photo:
        photo_file_id = message.photo[-1].file_id
        message_text = message.caption
        text_message = (f'Your message: {message_text}, '
                        f'latitude: {data.get("latitude")}, '
                        f'longitude: {data.get("longitude")}')
        await message.answer_photo(photo_file_id, caption=text_message)
    else:
        message_text = message.text
        text_message = (f'Your send only message: {message_text}, without photo, your coordinates: '
                        f'latitude: {data.get("latitude")}, '
                        f'longitude: {data.get("longitude")}')
        await message.answer(text_message)
        save_data = {
            'latitude': str(data.get("latitude")),
            'longitude': str(data.get("longitude")),
            'message': message_text,
            'user_id': 'd4eebf98-2d1a-46a4-8f3c-40eb247cbbcc'
        }
        await coordinate_service.create_coordinate(save_data)
    # todo: В случаи добавления изображений, это может долго обрабатываться,
    #  по этому нужно делать celery или отправлять пользователю, что все готово, а самому обновлять.

    await state.clear()
