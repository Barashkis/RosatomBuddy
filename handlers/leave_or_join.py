from loader import dp, bot
from logger import logger
from utils import db

from aiogram import types


@dp.my_chat_member_handler()
async def user_leave_or_join(update: types.ChatMemberUpdated):
    if update.new_chat_member.is_chat_member():
        leave = False

        user_id = update.from_user.id
        user = await db.get_user(user_id)

        skipped_publications = user["skipped_publications"].split()
        if skipped_publications:
            text = "С возвращением! За время твоего отсутствия были пропущены некоторые публикации:\n\n" + \
                   "\n\n".join([(await db.get_publication(int(publication_id)))["text"]
                                for publication_id in skipped_publications])

            await bot.send_message(user_id, text)

            await db.update_user(user_id, skipped_publications="")
    else:
        leave = True

    await db.update_user(update.chat.id, leave=leave)

    logger.debug(f"User {update.from_user.id} {'stopped' if leave else 'joined'} the bot")
