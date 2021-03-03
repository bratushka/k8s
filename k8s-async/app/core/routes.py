import asyncpg
from fastapi import APIRouter, HTTPException, Response
from neo4j.exceptions import ServiceUnavailable

from .services import Graph, Redis, SQL


router = APIRouter()


@router.get('/alive/')
async def alive():
    """
    Health check.
    """
    try:
        redis_alive = await Redis.alive()
        if not redis_alive:
            raise HTTPException(503, 'Redis responded badly.')
    except ConnectionResetError:
        raise HTTPException(503, 'Redis refused to connect.')

    try:
        graph_alive = Graph.alive()
        if not graph_alive:
            raise HTTPException(503, 'Redis responded badly.')
    except ServiceUnavailable:
        raise HTTPException(503, 'Graph refused to connect.')

    try:
        con: asyncpg.connection.Connection
        async with SQL.connection() as con:
            try:
                await con.fetchrow('SELECT true;', timeout=3)
            except TimeoutError:
                raise HTTPException(503, 'SQL connection timeout.')
    except OSError:
        raise HTTPException(503, 'SQL refused to connect.')

    return Response(status_code=204)
