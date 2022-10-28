from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils import db


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        admins = [admin["user_id"] for admin in await db.get_admins()]
        if message.from_user.id in admins:
            return True

        return False


class IsForwarded(BoundFilter):
    async def check(self, message: types.Message):
        if message.is_forward():
            return True

        return False


class IsFromUser(BoundFilter):
    async def check(self, message: types.Message):
        if message.forward_from.is_bot:
            return False

        return True
