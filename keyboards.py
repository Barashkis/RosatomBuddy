from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

divisions_cd = CallbackData("division", "choice")

accept_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Подтверждаю", callback_data="accept")]
    ]
)

is_trainer_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Да", callback_data="trainer_yes"), InlineKeyboardButton("Нет", callback_data="trainer_no")]
    ]
)

ready_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Я готов", callback_data="ready")]
    ]
)

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("История Росатома и интересные факты", callback_data="facts")],
        [InlineKeyboardButton("Лица Росатома", callback_data="faces")],
        [InlineKeyboardButton("Проекты Росатома", callback_data="projects")],
        [InlineKeyboardButton("Полезные ресурсы и ссылки", callback_data="faq")],
        [InlineKeyboardButton("Дивизионы", callback_data="divisions")],
        [InlineKeyboardButton("Полезная информация", callback_data="information")],
    ]
)


def from_list_kb(list_):
    kb = InlineKeyboardMarkup()

    for choice, element in enumerate(list_):
        kb.row(InlineKeyboardButton(text=element, callback_data=divisions_cd.new(choice=choice)))

    return kb
