import aiosqlite
import asyncpg
from contextlib import asynccontextmanager


async def init_connection(conn):
    await conn.execute("SET search_path TO content, public")


async def get_postgres_pool(POSTGRES_DSL) -> asyncpg.Pool:
    pool = await asyncpg.create_pool(**POSTGRES_DSL, init=init_connection)
    return pool


@asynccontextmanager
async def async_conn_context(db_path: str):
    conn = await aiosqlite.connect(db_path)
    try:
        conn.row_factory = aiosqlite.Row
        yield conn
    finally:
        await conn.close()


