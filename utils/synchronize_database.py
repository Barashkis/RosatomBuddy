import asyncio
import re

import gspread as gspread

from config import publications_link, posts_link, week_days
from .postgresql import db

gc = gspread.service_account_from_dict(
    {
        "type": "service_account",
        "project_id": "rosatom-buddy",
        "private_key_id": "59084aad2db2be355e5c53f91aedec6ea699d250",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDIvR0GQ3/cM0jK"
                       "\nOxoB1Ss5IY6u++87idfNU4FTH9/pvCYZhIVYkykWGIQQ9Dh0TynBgO/JI9UPsQMk\nEC"
                       "/J5yUe6CXLM9jFKHOB64FfhFLBbbO46vft7HV+jZ08XbaHHfh5E69Xw1T7HAgz\nT"
                       "+xgL9SUq1eeBwKihpvJxCTSAKFKzXSQD/YyZMHPKy8VP1kM3g+xAVZXtjkkkAar\nCBrzX+if50pXi"
                       "+8YPjyrHpdrPVwRI9hhEvWSIt0z4LNP8C+NNq/mbTosiJ28znoW\nV95yKjaGVLt1DNkj5gYsZD5+ssKiL8M"
                       "+dsXfwtbCUysOELX5HlWgMCwD5Ohw4DEH\nvpxXNAZ/AgMBAAECggEAFIFQ4i9p863fbRz9apuCV0sovpIonV3Wx"
                       "/gUOVADuOYJ\nxEiHsIUTyNiHQQ4ZaDQf8U7A77xzyq8LwZbPsuGkJpSTK78nkPgxWF+crwuewnh4\nx9Zkrg6d7"
                       "+f6XEy8VPAITiHnIuFmoGH8KnWrESZBolAgWpmfuMdkSYd6NWNwFmpY\n9cLu5vf9Zn7Lkualsw+lE"
                       "+FB2frDHTO42rCuoN9u3oH9w9Dh8Us8McxzsPGtalcd\nQYbhB7lk4V0Krt76OOtsAcuF"
                       "+ivJio2JknfvOtKidF7piGKt3+4fjWX0ZDwEY/Io\nd394XBKOn6FomfBvRNH5Oe9fYimkrYyQoEshTg"
                       "/SFQKBgQDtTLo9mZ7+cHr8z8uv\nTCQMZxeQbxR3uKDVrK234/d+et7+oiTCxexXLHocqOQcazKhL8EtQJFCRbHNkzSg"
                       "\nHpI+HZuX1bQh5b0dH4zbzF/iPpyrSOAfpot+tuBJej5y/VatIvwWK6a4XyxxAxiB"
                       "\nP8rJGUF1tZaohOH2M2CKPytvBQKBgQDYjs5mvz8V7m0ewt8nIo0m0CSin3lGSgCW\nrZGmtIvkdWtAVufNw/uH9R"
                       "/mkAxo91rU7b5dIIJhrLzhzUP1xG3XDkMe/spmOKd4\niPxQTc3zkfLXn3EvF/qCH6pljS"
                       "+qN7VL9oDUUSqHHtVrPD2pXcnwc92p8/FU7XS/\nwie/GuCuswKBgBKam1dM"
                       "/ewQwXOkjuF1ZLYcNvq52q7wKJvX596s3rBpzaXE7IDg\np4DGGeS5UPjxZozAg7Kah0jc0e2"
                       "+Brgu7WQ1SgeDV5X4vvTTjmWFBldkdT/wfLG"
                       "+\nit0qVTctgEvflLYKMh1C2tVFkORjS76GU82kTz99NwyLLnPw3za3cR5JAoGAeXzz"
                       "\n8dRMceNGOEGeqvfJNAME6m6IvJP7bIyG73zOFiaBOqEGffr6ezVa5h/dtm09+cI+\nT0RToLQlao"
                       "+bFp9R95m6sgLCTUJvQUGoOuzLI1+3WpvKBV9wW9uj3kCsgtOp06nA"
                       "\ncFvwfckgdX5gIUnKZii6LAP8WWa1XnZvkdhkP90CgYAs7CTllY92f4q7V3vW7sbB"
                       "\nXV9xnZ9y6GQP5itHhZPqhxXIAA21BVqypFpegJMlsPE9M4AJ9SWMrAqZ3sMBPTXf\nO9uJ6"
                       "+M6uIG0I1NPQ1S32oXHPh8/gImVciB0jM99gNxkrb2JPQh+UbOcrxO/D0He\nkW29h+zFwfdqtQMzG9QM2w==\n"
                       "-----END PRIVATE KEY-----\n",
        "client_email": "synchronize-database@rosatom-buddy.iam.gserviceaccount.com",
        "client_id": "100391273225059548900",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/synchronize-database%40rosatom"
                                "-buddy.iam.gserviceaccount.com "
    }
)


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
