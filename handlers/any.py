from aiogram import types

from loader import dp
from logger import logger


@dp.message_handler(content_types=types.ContentType.ANY)
async def send_message(message: types.Message):
    await message.answer("К сожалению, у меня нет ответа на это сообщение\n\n"
                         "Чтобы взаимодействовать со мной, используй главное меню - /menu")

    logger.debug(f"User {message.from_user.id} entered content that bot doesn't understand")
