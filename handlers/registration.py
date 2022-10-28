import asyncio
from datetime import datetime
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold

from loader import dp, bot
from logger import logger
from utils import db, track_week, send_previous_publications, mailing, set_default_commands
from keyboards import from_list_kb, divisions_cd, is_trainer_kb, ready_kb, main_menu_kb
from config import companies, divisions


async def finish_registration(call_or_message: Union[types.CallbackQuery, types.Message],
                              division: str, company: str = None, is_trainer: bool = False):
    user_id = call_or_message.from_user.id
    username = call_or_message.from_user.username
    date_of_registration = int(datetime.now().timestamp())

    await db.add_user(user_id, username, division, company, is_trainer, date_of_registration)

    await bot.send_message(user_id,
                           "В программу адаптации включено более 100 публикаций, "
                           "с которыми ты ознакомишься в течение 12 недель\n\n"
                           "🛎 Проверь, включены ли у тебя уведомления. У тебя все обязательно получится!",
                           reply_markup=ready_kb)

    logger.debug(f"User {call_or_message.from_user.id} finished registration successfully")


@dp.callback_query_handler(text="accept")
async def choose_division(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(f"{hbold('Выбери свой дивизион.')} Если предприятие, в котором ты работаешь, "
                              "не включено в дивизиональную структуру, нажми на пункт «Другой»",
                              reply_markup=from_list_kb(divisions))

    logger.debug(f"User {call.from_user.id} entered choose_division handler")


@dp.callback_query_handler(divisions_cd.filter())
async def choose_company_or_register(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.delete()

    division_index = int(callback_data["choice"])
    division = divisions[division_index]

    if division == "Другой":
        companies_text = "\n".join([f"{number}. {company}" for number, company in enumerate(companies, start=1)])

        await call.message.answer(f"{hbold('Выбери предприятие, в котором ты работаешь (ответить нужно цифрой).')} "
                                  "Например, если ты являешься сотрудником "
                                  "Корпоративной Академии Росатома, пришли мне цифру «1»\n\n"
                                  f"{companies_text}")
        await state.set_state("input_company")
    else:
        await finish_registration(call_or_message=call, division=division)

    logger.debug(f"User {call.from_user.id} entered choose_company_or_register handler and chose '{division}' division")


@dp.message_handler(state="input_company")
async def choose_role_or_register(message: types.Message, state: FSMContext):
    company_index = int(message.text) - 1
    if not 0 <= company_index < len(companies):
        raise ValueError(f"company number must be between 1 and {len(companies)} but bot got {company_index}")

    company = companies[company_index]
    if company == "Корпоративная Академия Росатома":
        await message.answer("Здорово, ты работаешь в Корпоративной Академии Росатома! "
                             "Расскажи, являешься ли ты тренером?",
                             reply_markup=is_trainer_kb)
    else:
        await finish_registration(call_or_message=message, division="Другой", company=company)

    await state.finish()

    logger.debug(f"User {message.from_user.id} entered choose_role_or_register handler and chose '{company}' company")


@dp.callback_query_handler(Text(startswith="trainer"))
async def choose_role_and_register(call: types.CallbackQuery):
    await call.message.delete()

    chosen_role = call.data.split("_")[1]

    logger.debug(f"User {call.from_user.id} entered choose_role_and_register handler and chose role '{'trainer' if chosen_role == 'yes' else 'user'}'")

    if chosen_role == "yes":
        await finish_registration(call_or_message=call, division="Другой", company="Корпоративная Академия Росатома",
                                  is_trainer=True)
    else:
        await finish_registration(call_or_message=call, division="Другой", company="Корпоративная Академия Росатома")


@dp.callback_query_handler(text="ready")
async def user_ready(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("🎉 Поздравляем, ты стал частью команды профессионалов и работаешь в Госкорпорации "
                              "«Росатом». В первую очередь тебе необходимо оформить документы в отделе кадров "
                              "предприятия\n\n "
                              "Также ты можешь познакомиться с нашей отраслью поближе! Я добавил разные разделы, "
                              "в которых ты можешь побольше узнать о Росатоме ⚛️",
                              reply_markup=main_menu_kb)

    await set_default_commands(dp)

    asyncio.create_task(track_week(call.from_user.id))
    asyncio.create_task(send_previous_publications(call.from_user.id))
    asyncio.create_task(mailing(call.from_user.id))

    logger.debug(f"User {call.from_user.id} entered user_ready handler")
