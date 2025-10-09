from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ContentType, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
# import aiogram.utils.markdown as fmt

from src.services import coordinate_service, user_service


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
    # todo: Тут можно поймать ошибку, что координаты можно отправить из телефона только, надо ее обработать.

    await message.answer('Отправь координаты.', reply_markup=location_keyboard)

    if not await user_service.check_user(message.from_user.id):
        await user_service.create_user_from_message(message)

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
            'user_id': f'{message.from_user.id}'
        }
        await coordinate_service.create_coordinate(save_data)

    await state.clear()
