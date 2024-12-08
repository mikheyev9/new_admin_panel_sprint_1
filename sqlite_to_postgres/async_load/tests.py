import aiosqlite
import asyncpg

from async_load import models
from async_load.etl import extract_data, transform_data
from collections.abc import Sequence
from typing import Type, Any


async def run_tests(sqlite_conn, pg_conn) -> None:
    await test_table(sqlite_conn, pg_conn, 'film_work', models.FilmWork)
    await test_table(sqlite_conn, pg_conn, 'genre', models.Genre)
    await test_table(sqlite_conn, pg_conn, 'person', models.Person)
    await test_table(sqlite_conn, pg_conn, 'genre_film_work', models.GenreFilmwork,
                     ('film_work_id', 'genre_id'))
    await test_table(sqlite_conn, pg_conn, 'person_film_work', models.PersonFilmWork,
                     ('film_work_id', 'person_id'))


async def test_table(sqlite_conn: aiosqlite.Connection,
                     pg_conn: asyncpg.Connection,
                     table_name: str,
                     model_class: Type[Any],
                     columns_to_check: Sequence[str] = ()
                     ) -> None:
    print(f"Testing table: {table_name}")

    async for sqlite_batch in extract_data(sqlite_conn, table_name):
        original_records = await transform_data(sqlite_batch, table_name)
        ids = [record.id for record in original_records]

        transferred_records = await pg_conn.fetch(
            f'SELECT * FROM content.{table_name} WHERE id = ANY($1::uuid[])',
            ids
        )
        transferred_records = [model_class(**record) for record in transferred_records]

        assert len(original_records) == len(transferred_records),\
            f"Mismatch in number of records for {table_name}"

        trans_dict = {record.id: record for record in transferred_records}

        for original in original_records:
            trans = trans_dict.get(original.id)
            assert trans is not None, f"Record with ID {original.id} not found in PostgreSQL"

            for column in columns_to_check:
                original_value = getattr(original, column)
                trans_value = getattr(trans, column)
                assert original_value == trans_value,\
                    f"Mismatch in column '{column}' for record ID {original.id}"

    print(f"All records match for {table_name}. Data transfer successful!")



