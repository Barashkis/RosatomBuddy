from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold

from loader import dp, bot
from utils import db
from keyboards import main_menu_kb


@dp.message_handler(Command("menu"))
async def main_menu(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Выбери раздел, который тебя интересует", reply_markup=main_menu_kb)


@dp.callback_query_handler(text="facts")
async def show_facts(call: types.CallbackQuery):
    pass


@dp.callback_query_handler(text="faces")
async def show_faces(call: types.CallbackQuery):
    pass


@dp.callback_query_handler(text="projects")
async def show_projects(call: types.CallbackQuery):
    pass


@dp.callback_query_handler(text="faq")
async def show_faq(call: types.CallbackQuery):
    pass


@dp.callback_query_handler(text="divisions")
async def show_divisions(call: types.CallbackQuery):
    pass


@dp.callback_query_handler(text="contacts")
async def show_contacts(call: types.CallbackQuery):
    pass
