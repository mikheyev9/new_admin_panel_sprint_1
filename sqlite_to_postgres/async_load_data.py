import asyncio

import aiosqlite
import asyncpg

from async_load.database import get_postgres_pool, async_conn_context
from async_load.etl import extract_data, transform_data, load_data
from async_load.tests import run_tests
from config import SQLITE_DB_PATH, POSTGRES_DSL_ASYNC

TABLES = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']

async def clear_tables(pg_conn):
    print("Clearing all tables in PostgreSQL...")
    for table in TABLES:
        await pg_conn.execute(f"TRUNCATE TABLE content.{table} CASCADE")
        sequence_exists = await pg_conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM information_schema.sequences "
            "WHERE sequence_schema = 'content' AND sequence_name = $1)",
            f"{table}_id_seq"
        )
        if sequence_exists:
            await pg_conn.execute(f"ALTER SEQUENCE content.{table}_id_seq RESTART WITH 1")
        else:
            print(f"Warning: Sequence 'content.{table}_id_seq' does not exist.")
    print("All tables cleared successfully")


async def process_table(sqlite_conn: aiosqlite.Connection,
                        pg_conn: asyncpg.Connection,
                        table_name: str) -> None:
    print(f"Processing table: {table_name}")
    records_processed = 0

    async for batch in extract_data(sqlite_conn, table_name):

        transformed_data = await transform_data(batch, table_name)

        await load_data(pg_conn, transformed_data, table_name)

        records_processed += len(transformed_data)
        print(f"Processed {records_processed} records for {table_name}")

    print(f"Finished processing {table_name}")


async def main():
    async with await get_postgres_pool(POSTGRES_DSL_ASYNC) as pg_pool:
        async with pg_pool.acquire() as pg_conn:
            async with async_conn_context(SQLITE_DB_PATH) as sqlite_conn:

                await clear_tables(pg_conn)

                for table_name in TABLES:
                    await process_table(sqlite_conn, pg_conn, table_name)

                print("All tables processed")

                await run_tests(sqlite_conn, pg_conn)
                print("Transfer test completed successfully")

    print('🎉 Данные успешно перенесены !!!')


if __name__ == '__main__':
    asyncio.run(main())