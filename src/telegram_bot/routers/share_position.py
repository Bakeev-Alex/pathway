from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, Message, ReplyKeyboardRemove

import aiogram.utils.markdown as fmt

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)

share_location_route = Router()


class ShareLocationState(StatesGroup):
    coordinates = State()
    comment = State()
    photo = State()


@share_location_route.message(Command('share_location'))
async def position_handler(message: Message, state: FSMContext):
    """Вступительное сообщение для получения координат по нажатию на кнопку."""
    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Отправить координаты', request_location=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

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
    photo_file_id = message.photo[-1].file_id

    data = await state.get_data()
    text_message = (f'Your message: {message.caption}, '
                    f'latitude: {data.get("latitude")}, '
                    f'longitude: {data.get("longitude")}')
    await message.answer_photo(photo_file_id, caption=text_message)
    await state.clear()
