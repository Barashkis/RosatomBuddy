from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from config import timezone
from filters import IsAdmin, IsForwarded, IsFromUser
from keyboards import admin_pagination_kb, admin_kb, admin_cd
from logger import logger
from utils import db
from loader import dp


@dp.message_handler(Command("admin"), IsAdmin())
async def admin_panel(message: types.Message):
    await message.answer("Выберите нужный пункт", reply_markup=admin_kb)

    logger.debug(f"Admin {message.from_user.id} entered /admin command")


@dp.callback_query_handler(admin_cd.filter())
async def admin_pagination(call: types.CallbackQuery, callback_data: dict):
    await call.message.delete()

    users = await db.get_all_users()
    if not users:
        await call.message.answer("В базе пока нету зарегистрированных пользователей...", reply_markup=admin_kb)

        logger.debug(f"Admin {call.from_user.id} entered admin_pagination handler but there wasn't any users in the database")

        return

    common_users = [user for user in users if not user['is_trainer']]

    page = int(callback_data["page"])
    user = users[page - 1]

    id_ = user["user_id"]
    date_of_registration = datetime.fromtimestamp(user["date_of_registration"]).astimezone(timezone).strftime("%d.%m.%Y %H:%M")
    username = user["username"] if user["username"] else "отсутствует"
    division = user["division"]
    company = user["company"] if user["company"] else "отсутствует"
    is_trainer = "да" if user["is_trainer"] else "нет"
    status = user["status"].lower()
    leave = "заблокирован" if user["leave"] else "работает"

    last_post_id = user["last_publication_id"]
    last_post = (await db.get_publication(last_post_id))["text"] if last_post_id else 'Пользователь пока не получал сообщений от бота'

    text = f"На данный момент в базе находится пользователей: {len(users)} ({len(common_users)} - обычных пользователей и {len(users) - len(common_users)} - тренеров)\n\n" \
           f"<b>ID пользователя:</b> {id_}\n" \
           f"<b>Дата регистрации:</b> {date_of_registration}\n" \
           f"<b>Имя в Telegram:</b> @{username}\n" \
           f"<b>Дивизион:</b> {division}\n" \
           f"<b>Предприятие:</b> {company}\n" \
           f"<b>Тренер:</b> {is_trainer}\n" \
           f"<b>Статус:</b> {status}\n" \
           f"<b>Состояние бота:</b> {leave}\n" \
           "<b>Последнее сообщение от бота:</b>\n\n" \
           f"{last_post}"

    await call.message.answer(text, reply_markup=admin_pagination_kb(users, page))

    logger.debug(f"Admin {call.from_user.id} entered admin_pagination handler with {page=}")


@dp.callback_query_handler(text="admins")
async def watch_admins(call: types.CallbackQuery):
    await call.message.delete()

    admins = await db.get_admins()

    await call.message.answer(f"На данный момент в базе находится админов: {len(admins)}", reply_markup=admin_kb)

    logger.debug(f"Admin {call.from_user.id} entered watch_admins handler")


@dp.callback_query_handler(text="add_admin")
async def add_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f"Перешлите в бота любое сообщение пользователя, которого хотите сделать админом")

    await state.set_state('adding_admin')

    logger.debug(f"Admin {call.from_user.id} entered add_admin handler")


@dp.message_handler(IsForwarded(), IsFromUser(), state='adding_admin')
async def adding_admin(message: types.Message, state: FSMContext):
    new_admin_id = message.forward_from.id

    admin_ids = [admin["user_id"] for admin in await db.get_admins()]
    if new_admin_id not in admin_ids:
        await db.add_admin(new_admin_id)

        text = "Пользователь был успешно добавлен в список админов бота"
    else:
        text = "Данный пользователь уже есть в списке админов бота"

    await message.answer(text, reply_markup=admin_kb)

    await state.finish()

    logger.debug(f"Admin {message.from_user.id} entered adding_admin handler and got text message {text=}")


@dp.message_handler(state='adding_admin')
async def message_is_not_forwarded(message: types.Message):
    await message.answer("Пожалуйста, перешлите сообщение другого пользователя. "
                         "Пользователь не может быть ботом.\n\n"
                         "Повторите попытку еще раз")

    logger.debug(f"Admin {message.from_user.id} entered message_is_not_forwarded handler")


@dp.callback_query_handler(text="close_list")
async def admin_panel(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Выберите нужный пункт", reply_markup=admin_kb)

    logger.debug(f"Admin {call.from_user.id} entered admin_panel handler")
