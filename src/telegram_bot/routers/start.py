import aiogram.utils.markdown as fmt

from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def command_start(message: types.Message) -> None:
    message_text = fmt.text(
        fmt.text('Приветствую тебя путник, ты здесь, значит ты на тропе\\.'),
        fmt.text('Этот бот поможет тебе делиться впечатлениями и эмоциям\\.'),
        fmt.text('Ты можешь отправлять свои координаты, фото и сообщение для других путников '
                 'и видеть их на карте в приложении\\.'),
        sep="\n"
    )
    message_text += fmt.text(
        fmt.text('\n\nТы можете воспользоваться одной из следующих функций: '),
        fmt.text('• /start \\-\\- Начальная страница\\.'),
        sep="\n",
    )

    await message.answer(
        message_text,
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode='MarkdownV2'
    )
