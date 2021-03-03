import ssl

import aioredis
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
    """
    Make it async when Neo4j driver complies.
    """
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
