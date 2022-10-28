import asyncio
import re

import gspread as gspread

from logger import logger
from config import publications_link, posts_link, week_days
from .postgresql import db

gc = gspread.service_account(filename="credentials.json")


async def sync_publications():
    while True:
        document = gc.open_by_url(publications_link)

        publication_id = 1
        for sheet in document:
            week = int(sheet.title.split()[-1])

            day, text, for_trainer, hour, minutes = [None] * 5
            for row in sheet.get_all_values():
                if row[0].strip() in week_days.keys():
                    day = week_days[row[0].strip()]
                elif row[0]:
                    if "в отрасли" in row[0]:
                        for_trainer = False
                    else:
                        for_trainer = True

                    try:
                        time = re.findall(r"(\d+:\d+)", row[0])[0].split(':')
                    except IndexError:
                        continue

                    hour, minutes = int(time[0]), int(time[1])

                if row[1]:
                    text = row[1]

                if not all([day, text, hour]):
                    continue

                current_publication = await db.get_publication(publication_id)

                if not current_publication:
                    await db.add_publication(text, week, day, hour, minutes, for_trainer)

                    logger.debug(f"Publication with {publication_id=} was added successfully")
                elif list(current_publication)[1:] != [text, week, day, hour, minutes, for_trainer]:
                    await db.update_publication(publication_id, text=text, week=week, day=day, hour=hour,
                                                minutes=minutes, for_trainer=for_trainer)

                    logger.debug(f"Publication with {publication_id=} was updated successfully")

                text, for_trainer, hour, minutes = [None] * 4

                publication_id += 1

        await asyncio.sleep(3600 * 24)

        logger.debug("Publications sheets were checked and synchronized with database successfully")


async def sync_posts():
    while True:
        document = gc.open_by_url(posts_link)

        post_id = 1
        for sheet in document:
            title = sheet.title.lower()

            if "история" in title:
                tag = "facts"
            elif "лица" in title:
                tag = "faces"
            elif "проекты" in title:
                tag = "projects"
            elif "ресурсы" in title:
                tag = "sources"
            else:
                tag = "information"

            row = sheet.row_values(1)[1:]
            for post in row:
                if post:
                    try:
                        photo = re.findall(r"https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}\.jpg", post)[0]
                    except IndexError:
                        photo = None

                    if photo:
                        text = post.replace(photo, "")
                    else:
                        text = post

                    current_post = await db.get_post(post_id)

                    if not current_post:
                        await db.add_post(tag, text, photo)

                        logger.debug(f"Post with {post_id=} was added successfully")
                    elif list(current_post)[1:] != [tag, text, photo]:
                        await db.update_post(post_id, tag=tag, text=text, photo=photo)

                        logger.debug(f"Post with {post_id=} was updated successfully")

                post_id += 1

        await asyncio.sleep(3600 * 24)

        logger.debug("Posts sheets were checked and synchronized with database successfully")
