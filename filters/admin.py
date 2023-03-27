from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils import db


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return message.from_user.id in [admin["user_id"] for admin in await db.get_admins()]


class IsForwarded(BoundFilter):
    async def check(self, message: types.Message):
        return message.is_forward()


class IsFromUser(BoundFilter):
    async def check(self, message: types.Message):
        return message.forward_from.is_bot
