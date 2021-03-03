import logging

from fastapi import APIRouter, HTTPException
from neo4j.exceptions import ServiceUnavailable

from .services import Graph, Redis


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/alive/')
async def alive():
    """
    Health check.
    """
    try:
        redis_alive = await Redis.alive()
        if not redis_alive:
            raise HTTPException(503, 'Redis responded badly')
    except ConnectionResetError:
        raise HTTPException(503, 'Redis refused to connect')
    try:
        graph_alive = Graph.alive()
        if not graph_alive:
            raise HTTPException(503, 'Redis responded badly')
    except ServiceUnavailable:
        raise HTTPException(503, 'Graph refused to connect')

    return True
