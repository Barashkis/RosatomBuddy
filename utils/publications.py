from datetime import datetime
import asyncio

from aiogram.utils.exceptions import TelegramAPIError

from logger import logger
from .postgresql import db
from config import timezone
from loader import bot


async def send_previous_publications(user_id: int, status: str, leave: bool):
    if status == "Догоняет публикации" and leave is False:
        first_week_publications = await db.get_publications(week=1)
        for publication in first_week_publications:
            user = await db.get_user(user_id)

            today = datetime.today().astimezone(timezone)

            current_week_day = today.isoweekday()
            current_hour = today.hour
            current_minutes = today.minute

            if user["week"] == 2 or publication["day"] < current_week_day or \
                    (publication["day"] == current_week_day and (publication["hour"] < current_hour
                     or publication["hour"] == current_hour and publication["minutes"] <= current_minutes)):
                if publication["for_trainer"] and not user["is_trainer"]:
                    continue

                await asyncio.sleep(1800)

                try:
                    await bot.send_message(user_id, publication["text"])
                except TelegramAPIError:
                    return
                else:
                    await db.update_user(user_id, last_publication_id=publication["id"])

                    logger.debug(f"User {user_id} got first week catch-up publication")

        await db.update_user(user_id, status="Получает публикации по расписанию")

        logger.debug(f"User {user_id} got all first week catch-up publications and now he's getting publications on schedule")


async def mailing(user_id):
    while True:
        user = await db.get_user(user_id)
        if user["status"] == "Получает публикации по расписанию" and user["leave"] is False:
            today = datetime.today().astimezone(timezone)

            current_week_day = today.isoweekday()
            current_hour = today.hour
            current_minutes = today.minute

            week = user["week"]

            publications = await db.get_publications(week=week)
            for i in range(len(publications)):
                publication = publications[i]
                if publication["for_trainer"] and not user["is_trainer"]:
                    continue

                if publication["hour"] == current_hour and publication["day"] == current_week_day \
                        and publication["minutes"] == current_minutes \
                        and user["last_publication_id"] != publication["id"]:
                    try:
                        await bot.send_message(user_id, publication["text"])
                    except TelegramAPIError:
                        pass
                    else:
                        await db.update_user(user_id, last_publication_id=publication["id"])

                        logger.debug(f"User {user_id} got publication with {week=}")

            await asyncio.sleep(59)


async def track_week():
    while True:
        previous_week = datetime.today().astimezone(timezone).isocalendar()[1]

        await asyncio.sleep(60)

        current_week = datetime.today().astimezone(timezone).isocalendar()[1]

        if current_week == previous_week + 1:
            await db.next_week()

            logger.debug(f"Week was updated to all users")
