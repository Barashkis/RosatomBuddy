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
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL NOT NULL,
        user_id BIGINT,
        username VARCHAR(100),
        division VARCHAR(100),
        company VARCHAR(100),
        week INT DEFAULT 1,
        is_trainer BOOLEAN,
        date_of_registration BIGINT,
        status VARCHAR(100) DEFAULT 'Догоняет публикации',
        leave BOOLEAN DEFAULT FALSE,
        PRIMARY KEY (user_id)
        );

        CREATE TABLE IF NOT EXISTS Publications (
        id SERIAL NOT NULL,
        text VARCHAR DEFAULT NULL,
        week INT,
        day INT,
        hour INT,
        minutes INT,
        for_trainer BOOLEAN,
        PRIMARY KEY (id)
        );
        
        CREATE TABLE IF NOT EXISTS Posts (
        id SERIAL NOT NULL,
        
        PRIMARY KEY (id)
        );
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(arguments: dict):
        query = ", ".join([f"{column} = ${number}" for number, column in enumerate(arguments.keys(), start=2)])

        return query

    async def add_user(self, user_id: int, username: str, division: str,
                       company: str, is_trainer: bool, date_of_registration: int):
        sql = """
        INSERT INTO Users (user_id, username, division, company, is_trainer, date_of_registration) 
        VALUES ($1, $2, $3, $4, $5, $6);
        """
        await self.pool.execute(sql, user_id, username, division, company, is_trainer, date_of_registration)

    async def add_publication(self, text: str, week: int, day: int, hour: int, minutes: int, for_trainer: bool):
        sql = """
        INSERT INTO Publications (text, week, day, hour, minutes, for_trainer) 
        VALUES ($1, $2, $3, $4, $5, $6);
        """
        await self.pool.execute(sql, text, week, day, hour, minutes, for_trainer)

    async def get_user(self, user_id: int):
        sql = f"""
        SELECT * FROM Users 
        WHERE user_id = $1;
        """
        return await self.pool.fetchrow(sql, user_id)

    async def get_publication(self, week: int, day: int, hour: int, minutes: int, for_trainer: bool):
        sql = f"""
        SELECT * FROM Publications 
        WHERE week = $1 AND day = $2 AND hour = $3 AND minutes = $4 AND for_trainer = $5;
        """
        return await self.pool.fetchrow(sql, week, day, hour, minutes, for_trainer)

    async def get_publications(self, week: int):
        sql = f"""
        SELECT * FROM Publications 
        WHERE week = $1;
        """
        return await self.pool.fetch(sql, week)

    async def update_user(self, user_id: int, **kwargs):
        sql = f"""
        UPDATE Users 
        SET {self.format_args(kwargs)} 
        WHERE user_id = $1;
        """
        return await self.pool.execute(sql, user_id, *kwargs.values())

    async def update_publication(self, publication_id: int, **kwargs):
        sql = f"""
        UPDATE Publications 
        SET {self.format_args(kwargs)} 
        WHERE id = $1;
        """
        return await self.pool.execute(sql, publication_id, *kwargs.values())


db = Database(loop=asyncio.get_event_loop())
