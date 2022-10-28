from loader import dp
from logger import logger
from utils import db

from aiogram import types


@dp.my_chat_member_handler()
async def user_leave_or_join(update: types.ChatMemberUpdated):
    if update.new_chat_member.is_chat_member():
        leave = False
    else:
        leave = True

    await db.update_user(update.chat.id, leave=leave)

    logger.debug(f"User {update.from_user.id} {'stopped' if leave else 'joined'} the bot")
