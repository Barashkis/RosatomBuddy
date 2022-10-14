import asyncio
import re

import gspread as gspread

from config import publications_link, posts_link, week_days
from .postgresql import db

gc = gspread.service_account_from_dict()


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

                current_publication = await db.get_publication(week, day, hour, minutes, for_trainer)

                if not current_publication:
                    await db.add_publication(text, week, day, hour, minutes, for_trainer)
                elif list(current_publication)[1:] != [text, week, day, hour, minutes, for_trainer]:
                    await db.update_publication(publication_id, text=text, week=week, day=day, hour=hour, minutes=minutes, for_trainer=for_trainer)

                text, for_trainer, hour, minutes = [None] * 4

                publication_id += 1

        await asyncio.sleep(300)


async def sync_posts():
    while True:
        document = gc.open_by_url(posts_link)

        for sheet in document:
            counter = 1
            if sheet.title == "История Росатома":
                theme = "RFACTS"
            elif sheet.title == "Люди Росатома":
                theme = 'RFACES'
            elif sheet.title == 'Проекты Росатома':
                theme = 'RPROJ'
            elif sheet.title == 'Полезные ресурсы и ссылки':
                theme = 'FAQ'
            elif sheet.title == 'Дивизионы':
                theme = 'DIVISIONS'
            else:
                theme = 'UINFO'
            for row in sheet.get_all_values():
                if row[0]:
                    if len(row) > 1 and 'http' in row[1]:
                        photo = row[1]
                    else:
                        photo = None
                    text = row[0]
                    if not await db.menu_posts.count_documents({'uid': counter, 'theme': theme}):
                        db.menu_posts.insert_one(
                            {'uid': counter, 'text': text.replace('\n', '\n\n'), 'photo': photo,
                             'theme': theme})
                    else:
                        db.menu_posts.update_one(
                            {'uid': counter, 'theme': theme},
                            {"$set": {'text': text.replace('\n', '\n\n'), 'photo': photo}})
                    counter += 1
            await db.users.update_many({theme: {'$gte': counter}}, {'$set': {theme: counter}})
            await db.menu_posts.delete_many({'theme': theme, 'uid': {'$gte': counter}})

        await asyncio.sleep(1800)
