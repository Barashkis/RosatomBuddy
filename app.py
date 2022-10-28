import asyncio

from aiogram import executor

import filters

from handlers import dp
from logger import logger
from utils import db, sync_publications, sync_posts, mailing, send_previous_publications
from config import admin_id


async def on_startup(_):
    await db.create_all_tables()

    admins = [admin["user_id"] for admin in await db.get_admins()]
    if admin_id not in admins:
        await db.add_admin(admin_id)

    logger.debug("Admins were added to the database successfully")

    users = await db.get_all_users()
    for user in users:
        asyncio.create_task(send_previous_publications(user["user_id"]))
        asyncio.create_task(mailing(user["user_id"]))

    logger.debug("Tasks to all users were added successfully")

    filters.setup(dp)

    logger.debug("Filters were set up successfully")

    asyncio.create_task(sync_publications())
    asyncio.create_task(sync_posts())

    logger.debug("Tasks to synchronize Google Sheets with database added successfully")

    logger.debug("Bot started successfully")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
