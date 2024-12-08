import sqlite3
from typing import Generator, Tuple, List, Any
from contextlib import contextmanager


@contextmanager
def cursor_context(connection: sqlite3.Connection) -> Generator[sqlite3.Cursor, None, None]:
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row
    try:
        yield cursor
    finally:
        cursor.close()


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.tables = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']

    def load_movies(self, batch_size: int = 100) -> Generator[Tuple[str, List[Any]], None, None]:
        with cursor_context(self.connection) as cursor:
            for table in self.tables:
                cursor.execute(f"SELECT * FROM {table}")
                while batch := cursor.fetchmany(batch_size):
                    yield table, batch
