from typing import Generator, Tuple, List, Any

from psycopg import connection as _connection
from psycopg.cursor import Cursor

from sync_load.sqlite_loader import SQLiteLoader
from sync_load.queries import SQL_QUERIES
from sync_load.transform_data import normalize_data
from sync_load.tests import run_tests



class PostgresSaver:
    def __init__(self,
                 pg_conn: _connection,
                 sqlite_loader: SQLiteLoader):
        self.pg_conn = pg_conn
        self.sqlite_loader = sqlite_loader


    def save_all_data(self,
                      data: Generator[Tuple[str, List[List[Any]]], None, None],
                      ) -> None:
        with self.pg_conn.cursor() as cursor:
            for table_name, rows in data:
                normalized_data = normalize_data(table_name, rows)
                self._save_table_data(cursor, table_name, normalized_data)
            run_tests(self.sqlite_loader, cursor)
            self.pg_conn.commit()


    def _save_table_data(self,
                         cursor: Cursor,
                         table_name: str,
                         rows: List[List[Any]]) -> None:
        query = SQL_QUERIES.get(table_name)
        if not query:
            raise ValueError(f"Unknown table: {table_name}")

        cursor.executemany(query, [row.__dict__ for row in rows])
