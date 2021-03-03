import ssl
# noinspection PyPep8Naming
import typing as T
from contextlib import asynccontextmanager

import aioredis
import asyncpg
from neo4j import GraphDatabase, Neo4jDriver, Session

from .. import config


class Service:
    """Common parent for all services."""


class Redis(Service):
    _pool: aioredis.Redis = None

    @classmethod
    async def pool(cls) -> aioredis.Redis:
        if cls._pool is None:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            cls._pool = await aioredis.create_redis_pool(
                'rediss://redis:6379',
                ssl=ssl_context,
                password=config.REDIS_PASSWORD,
            )

        return cls._pool

    @classmethod
    async def alive(cls) -> bool:
        pool = await cls.pool()
        pong = await pool.ping()

        return bool(pong)


class Graph(Service):
    _driver: Neo4jDriver = None

    @classmethod
    def driver(cls) -> Neo4jDriver:
        if cls._driver is None:
            cls._driver = GraphDatabase.driver(
                'neo4j+ssc://graph',
                auth=tuple(config.NEO4J_AUTH.split('/')),
            )

        return cls._driver

    @classmethod
    def session(cls) -> Session:
        return cls.driver().session()

    @classmethod
    def alive(cls) -> bool:
        with cls.session() as session:
            result = session.run('RETURN 1')

            return list(result)[0]['1'] == 1


class SQL:
    """
    Database class.
    """
    _pool: asyncpg.pool.Pool = None

    @classmethod
    @asynccontextmanager
    async def connection(cls) -> T.AsyncIterator[asyncpg.connection.Connection]:
        if cls._pool is None:
            cls._pool = await asyncpg.pool.create_pool(
                host='sql',
                port=5432,
                user=config.POSTGRES_USER,
                database=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
            )

        con: asyncpg.connection.Connection = await cls._pool.acquire()
        try:
            yield con
        finally:
            await cls._pool.release(con)
