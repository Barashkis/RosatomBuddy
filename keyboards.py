from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

divisions_cd = CallbackData("division", "choice")
main_menu_cd = CallbackData("topic", "tag", "page")
admin_cd = CallbackData("user", "page")

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
        [InlineKeyboardButton("История Росатома и интересные факты", callback_data=main_menu_cd.new(tag="facts", page=1))],
        [InlineKeyboardButton("Лица Росатома", callback_data=main_menu_cd.new(tag="faces", page=1))],
        [InlineKeyboardButton("Проекты Росатома", callback_data=main_menu_cd.new(tag="projects", page=1))],
        [InlineKeyboardButton("Полезные ресурсы и ссылки", callback_data=main_menu_cd.new(tag="sources", page=1))],
        [InlineKeyboardButton("Полезная информация", callback_data=main_menu_cd.new(tag="information", page=1))],
    ]
)

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Пользователи", callback_data=admin_cd.new(page=1))],
        [InlineKeyboardButton("Админы", callback_data="admins")],
        [InlineKeyboardButton("Добавить админа", callback_data="add_admin")]
    ]
)


def main_menu_pagination_kb(posts: list, tag: str, page: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    if len(posts) > 1:
        if page == 1:
            kb.row(InlineKeyboardButton("➡", callback_data=main_menu_cd.new(tag=tag, page=page + 1)))
        elif page == len(posts):
            kb.row(InlineKeyboardButton("⬅", callback_data=main_menu_cd.new(tag=tag, page=page - 1)))
        else:
            kb.row(InlineKeyboardButton("⬅", callback_data=main_menu_cd.new(tag=tag, page=page - 1)))
            kb.insert(InlineKeyboardButton("➡", callback_data=main_menu_cd.new(tag=tag, page=page + 1)))

    kb.row(InlineKeyboardButton("Назад", callback_data="main_menu"))

    return kb


def admin_pagination_kb(users: list, page: int = 1) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    if len(users) > 1:
        if page == 1:
            kb.row(InlineKeyboardButton("➡", callback_data=admin_cd.new(page=page + 1)))
        elif page == len(users):
            kb.row(InlineKeyboardButton("⬅", callback_data=admin_cd.new(page=page - 1)))
        else:
            kb.row(InlineKeyboardButton("⬅", callback_data=admin_cd.new(page=page - 1)))
            kb.insert(InlineKeyboardButton("➡", callback_data=admin_cd.new(page=page + 1)))

    kb.row(InlineKeyboardButton("Закрыть список", callback_data="close_list"))

    return kb


def from_list_kb(list_: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()

    for choice, element in enumerate(list_):
        kb.row(InlineKeyboardButton(text=element, callback_data=divisions_cd.new(choice=choice)))

    return kb
