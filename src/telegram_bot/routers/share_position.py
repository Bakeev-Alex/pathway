from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types, F
import random

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
async def get_share_position(message: Message, state: ShareLocationState):
    await message.answer('Отправь коодинаты.')
