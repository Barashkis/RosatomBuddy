from datetime import datetime
import asyncio

from aiogram.utils.exceptions import TelegramAPIError

from logger import logger
from .postgresql import db
from config import timezone
from loader import bot


async def send_previous_publications(user_id: int, status: str):
    if status == "Догоняет публикации":
        first_week_publications = await db.get_publications(week=1)
        for publication in first_week_publications:
            user = await db.get_user(user_id)

            today = datetime.today().astimezone(timezone)

            current_week_day = today.isoweekday()
            current_hour = today.hour
            current_minutes = today.minute

            if (user["week"] == 2 or (publication["day"] < current_week_day or
               (publication["day"] == current_week_day and (publication["hour"] < current_hour
                or publication["hour"] == current_hour and publication["minutes"] <= current_minutes)))) and \
                    user["last_publication_id"] < publication["id"]:
                if publication["for_trainer"] and not user["is_trainer"]:
                    continue

                await asyncio.sleep(1800)

                try:
                    await bot.send_message(user_id, publication["text"])

                    logger.debug(f"User {user_id} got first week catch-up publication")
                except TelegramAPIError:
                    skipped_publications = user["skipped_publications"].split()
                    skipped_publications.append(str(publication["id"]))
                    skipped_publications = " ".join(skipped_publications)

                    await db.update_user(user_id, skipped_publications=skipped_publications)

                    logger.debug(f"User {user_id} skipped first week catch-up publication")

                await db.update_user(user_id, last_publication_id=publication["id"])

        await db.update_user(user_id, status="Получает публикации по расписанию")

        logger.debug(f"User {user_id} got all first week catch-up publications and now he's getting publications on schedule")


async def mailing(user_id):
    while True:
        user = await db.get_user(user_id)
        if user["status"] == "Получает публикации по расписанию":
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

                        logger.debug(f"User {user_id} got publication with {week=}")
                    except TelegramAPIError:
                        skipped_publications = user["skipped_publications"].split()
                        skipped_publications.append(str(publication["id"]))
                        skipped_publications = " ".join(skipped_publications)

                        await db.update_user(user_id, skipped_publications=skipped_publications)

                        logger.debug(f"User {user_id} skipped publication with {week=}")

                    await db.update_user(user_id, last_publication_id=publication["id"])

                    last_publication = await db.get_latest_publication(user["is_trainer"])
                    if last_publication["id"] == publication["id"]:
                        await db.update_user(user_id, status="Прошел программу адаптации")
        elif user["status"] == "Прошел программу адаптации":
            logger.debug(f"User {user_id} finished adaptation program")

            break

        await asyncio.sleep(59)


async def track_week():
    while True:
        previous_week = datetime.today().astimezone(timezone).isocalendar()[1]

        await asyncio.sleep(60)

        current_week = datetime.today().astimezone(timezone).isocalendar()[1]

        if current_week == previous_week + 1:
            await db.next_week()

            logger.debug(f"Week was updated to all users")
