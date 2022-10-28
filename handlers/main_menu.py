from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsRegistered
from loader import dp
from logger import logger
from utils import db
from keyboards import main_menu_kb, main_menu_pagination_kb, main_menu_cd


@dp.message_handler(Command("menu"))
async def main_menu(message: types.Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if user:
        await message.answer("Выбери раздел, который тебя интересует", reply_markup=main_menu_kb)

        logger.debug(f"User {message.from_user.id} entered /menu command and got main_menu_kb")
    else:
        await message.answer("Кажется, ты еще не зарегистрировался...\n\n"
                             "Главное меню будет доступно сразу после регистрации - /start")

        logger.debug(f"User {message.from_user.id} entered /menu command but he hasn't registered yet")


@dp.callback_query_handler(IsRegistered(), text="main_menu")
async def back_to_main_menu(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Выбери раздел, который тебя интересует", reply_markup=main_menu_kb)

    logger.debug(f"User {call.from_user.id} entered back_to_main_menu handler")


@dp.callback_query_handler(IsRegistered(), main_menu_cd.filter())
async def show_posts(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()

    tag = callback_data["tag"]
    page = int(callback_data["page"])

    posts = await db.get_posts(tag)

    post = posts[page - 1]
    kb = main_menu_pagination_kb(posts, tag, page)

    text = post["text"]
    photo = post["photo"]

    if photo:
        await call.message.answer_photo(photo=photo, caption=text, reply_markup=kb)

        logger.debug(f"User {call.from_user.id} entered show_posts handler with {tag=} and {page=} and got post with with photo")
    else:
        await call.message.answer(text, reply_markup=kb)

        logger.debug(f"User {call.from_user.id} entered show_posts handler with {tag=} and  {page=} and got text post")


@dp.callback_query_handler(text="main_menu")
@dp.callback_query_handler(main_menu_cd.filter())
async def show_posts(call: types.CallbackQuery):
    await call.answer()

    await call.message.answer("Кажется, ты еще не зарегистрировался...\n\n"
                              "Главное меню будет доступно сразу после регистрации - /start")

    logger.debug(f"User {call.from_user.id} entered show_posts handler but he hasn't registered yet")
