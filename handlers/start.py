from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.markdown import hlink

from loader import dp
from utils import db
from keyboards import accept_kb, main_menu_kb


@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if user:
        await message.delete()
        await message.answer("Выбери раздел, который тебя интересует", reply_markup=main_menu_kb)
    else:
        await message.answer_sticker("CAACAgIAAxkBAAMGYVllOhTCuyx9DP8vOeswNLQ5WoMAAioDAALPu9QOH_K1GH9lnzAhBA")
        await message.answer("👋Привет! Меня зовут Бадди, я буду сопровождать тебя на протяжении 12 недель: "
                             "делиться, помогать, напоминать и, конечно же, вдохновлять\n\n"
                             "Я расскажу тебе про важные исторические события атомной отрасли, известных людей, "
                             "труды которых помогали и помогают развивать атомную промышленность, поделюсь "
                             "с тобой информацией о проектах, которыми мы по праву гордимся ⚛️\n\n"
                             "Ты узнаешь об основных направлениях деятельности дивизионов, получишь справочные "
                             "ресурсы для полного погружения в атмосферу крупнейшей научно-технологической "
                             "компании страны и познакомишься с корпоративными программами, проектами, "
                             "направлениями, чемпионатами и другими активностями, тебе точно понравится! 🔥")

        await message.answer(
            f"Подтвердите, что вы знакомы с "
            f"{hlink('политикой конфиденциальности персональных данных Госкорпорации «Росатом»', 'https://www.rosatom.ru/upload/iblock/cca/ccaff8fd4eab182ebd0e347053cd7945.pdf')}"
            " и принимаете её",
            reply_markup=accept_kb)
