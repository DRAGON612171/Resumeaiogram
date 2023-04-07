import asyncpg
from Resumeaiogram import config


class Database:
    def __init__(self):
        self.user = config.Server_username
        self.password = config.Server_password
        self.database = config.Database
        self.host = config.Server_host
        self.port = config.Server_port
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(user=self.user, password=self.password,
                                            database=self.database, host=self.host, port=self.port)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def execute(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)
