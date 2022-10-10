from datetime import datetime

import aiogram
import asyncio

from aiogram.utils.exceptions import BotBlocked

from .postgresql import db


async def send_previous_publications(user_id: int, bot: aiogram.Bot):
    user = await db.get_user(user_id)

    today = datetime.today()
    current_week_day = today.isoweekday()
    current_hour = today.hour
    current_minutes = today.minute

    first_week_publications = await db.get_publications(week=1)
    for publication in first_week_publications:
        if publication["day"] <= current_week_day and \
                (publication["hour"] <= current_hour or
                 publication["hour"] <= current_hour and publication["minutes"] <= current_minutes):
            if publication["for_trainer"] and not user["is_trainer"]:
                continue

            await asyncio.sleep(1800)

            try:
                await bot.send_message(user_id, publication["text"])
            except BotBlocked:
                return

    await db.update_user(user_id, status="Получает публикации по расписанию")


async def mailing(user_id: int, bot: aiogram.Bot):
    while True:
        today = datetime.today()
        current_week_day = today.isoweekday()
        current_hour = today.hour
        current_minutes = today.minute

        user = await db.get_user(user_id)
        week = user["week"]
        status = user["status"]

        skipped_publications = []

        publications = await db.get_publications(week=week)
        for publication in publications:
            if publication["for_trainer"] and not user["is_trainer"]:
                continue

            if publication["hour"] == current_hour and publication["minutes"] == current_minutes \
                    and publication["day"] == current_week_day:
                if status == "Догоняет публикации":
                    skipped_publications.append(publication)
                else:
                    await bot.send_message(user_id, publication["text"])

        if status == "Получает публикации по расписанию" and skipped_publications:
            for skipped_publication in skipped_publications:
                await bot.send_message(user_id, skipped_publication["text"])

        await asyncio.sleep(60)


async def track_week(user_id: int):
    while True:
        previous_week = datetime.today().isocalendar()[1]

        await asyncio.sleep(60)

        current_week = datetime.today().isocalendar()[1]

        if current_week == previous_week + 1:
            user = await db.get_user(user_id)
            week = user["week"]

            await db.update_user(user_id, week=week + 1)
