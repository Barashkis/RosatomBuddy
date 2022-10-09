from aiogram import executor

from handlers import dp


async def on_startup(_):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
