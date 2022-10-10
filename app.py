import asyncio

from aiogram import executor

from handlers import dp
from utils import db, sync_publications


async def on_startup(_):
    await db.create_all_tables()
    await dp.bot.delete_my_commands()

    asyncio.create_task(sync_publications())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
