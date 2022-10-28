from aiogram import Dispatcher

from .admin import IsAdmin, IsForwarded, IsFromUser
from .user import IsRegistered


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsForwarded)
    dp.filters_factory.bind(IsFromUser)
    dp.filters_factory.bind(IsRegistered)
