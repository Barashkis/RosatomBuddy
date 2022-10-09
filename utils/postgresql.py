import asyncio
import asyncpg

import config


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncpg.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.pg_user,
                password=config.pg_pass,
                host=config.pg_host,
                database=config.pg_db_name
            )
        )

    async def create_all_tables(self):
        pass

    async def add_user(self, user_id: int, username: str, division: str,
                       company: str, is_trainer: bool, date_of_registration: int):
        pass

    async def get_user(self, user_id: int):
        pass
