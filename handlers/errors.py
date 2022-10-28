from aiogram.types import Update

from loader import dp
from logger import logger


@dp.errors_handler()
async def catch_errors(update: Update, exception):
    if isinstance(exception, ValueError):
        await update.get_current().message.answer("В результате обработки запроса возникла ошибка... "
                                                  "Попробуй еще раз")

        logger.debug(f"User {update.message.from_user.id} got an exception: {exception}")

        return
