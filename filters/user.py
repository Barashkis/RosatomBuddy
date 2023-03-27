from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils import db


class IsRegistered(BoundFilter):
    async def check(self, message: types.Message):
        users = [user["user_id"] for user in await db.get_all_users()]

        return message.from_user.id in users
