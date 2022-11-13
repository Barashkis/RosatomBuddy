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
        CREATE TABLE IF NOT EXISTS Admins (
        id SERIAL NOT NULL,
        user_id BIGINT,
        PRIMARY KEY (user_id)
        );
        
        CREATE TABLE IF NOT EXISTS Posts (
        id SERIAL NOT NULL,
        tag VARCHAR(20),
        text VARCHAR,
        photo VARCHAR,
        PRIMARY KEY (id)
        );
        
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
        last_publication_id INT DEFAULT 0,
        leave BOOLEAN DEFAULT FALSE,
        PRIMARY KEY (user_id)
        );

        CREATE TABLE IF NOT EXISTS Publications (
        id SERIAL NOT NULL,
        text VARCHAR,
        week INT,
        day INT,
        hour INT,
        minutes INT,
        for_trainer BOOLEAN,
        PRIMARY KEY (id)
        );
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(arguments: dict):
        query = ", ".join([f"{column} = ${number}" for number, column in enumerate(arguments.keys(), start=2)])

        return query

    async def add_admin(self, user_id: int):
        sql = """
        INSERT INTO Admins (user_id) 
        VALUES ($1);
        """
        await self.pool.execute(sql, user_id)

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

    async def add_post(self, tag: str, text: str, photo: str):
        sql = """
        INSERT INTO Posts (tag, text, photo) 
        VALUES ($1, $2, $3);
        """
        await self.pool.execute(sql, tag, text, photo)

    async def get_user(self, user_id: int):
        sql = f"""
        SELECT * FROM Users 
        WHERE user_id = $1;
        """
        return await self.pool.fetchrow(sql, user_id)

    async def get_publication(self, publication_id: int):
        sql = f"""
        SELECT * FROM Publications 
        WHERE id = $1;
        """
        return await self.pool.fetchrow(sql, publication_id)

    async def get_post(self, post_id: int):
        sql = f"""
        SELECT * FROM Posts 
        WHERE id = $1;
        """
        return await self.pool.fetchrow(sql, post_id)

    async def get_admins(self):
        sql = f"""
        SELECT * FROM Admins; 
        """
        return await self.pool.fetch(sql)

    async def get_all_users(self):
        sql = f"""
        SELECT * FROM Users; 
        """
        return await self.pool.fetch(sql)

    async def get_publications(self, week: int):
        sql = f"""
        SELECT * FROM Publications 
        WHERE week = $1;
        """
        return await self.pool.fetch(sql, week)

    async def get_latest_publication(self, is_trainer: bool):
        sql = f"""
        SELECT * FROM Publications 
        WHERE for_trainer = {is_trainer}
        ORDER BY week DESC, id DESC
        LIMIT 1;
        """
        return await self.pool.fetchrow(sql)

    async def get_posts(self, tag: str):
        sql = f"""
        SELECT * FROM Posts 
        WHERE tag = $1;
        """
        return await self.pool.fetch(sql, tag)

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

    async def update_post(self, post_id: int, **kwargs):
        sql = f"""
        UPDATE Posts 
        SET {self.format_args(kwargs)} 
        WHERE id = $1;
        """
        return await self.pool.execute(sql, post_id, *kwargs.values())

    async def next_week(self):
        sql = f"""
        UPDATE Users 
        SET week = week + 1;
        """
        return await self.pool.execute(sql)


db = Database(loop=asyncio.get_event_loop())
