import sqlite3
from typing import Generator, Tuple, List, Any

import psycopg
from psycopg import connect
from psycopg.rows import dict_row

from sync_load.sqlite_loader import SQLiteLoader
from sync_load.postgres_saver import PostgresSaver
from sync_load.clear import clear_tables
from config import SQLITE_DB_PATH, POSTGRES_DSL

print(POSTGRES_DSL)

TABLES = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']


def load_from_sqlite(connection: sqlite3.Connection,
                     pg_connection: psycopg.Connection) -> None:
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver = PostgresSaver(pg_connection, sqlite_loader)

    data: Generator[Tuple[str, List[List[Any]]], None, None] = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)



if __name__ == '__main__':
    with sqlite3.connect(SQLITE_DB_PATH) as sqlite_conn, connect(
        **POSTGRES_DSL, row_factory=dict_row
    ) as pg_conn:

        clear_tables(pg_conn, TABLES)

        load_from_sqlite(sqlite_conn, pg_conn)
