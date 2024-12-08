from collections.abc import Sequence
from typing import Generator, Tuple, List, Any, Type
from psycopg.cursor import Cursor

import sync_load.models as models
from sync_load.sqlite_loader import SQLiteLoader
from sync_load.transform_data import normalize_data

table_config = {
    'film_work': (models.FilmWork, ()),
    'genre': (models.Genre, ()),
    'person': (models.Person, ()),
    'genre_film_work': (models.GenreFilmwork, ('film_work_id', 'genre_id')),
    'person_film_work': (models.PersonFilmWork, ('film_work_id', 'person_id')),
}

def run_tests(sqlite_loader: SQLiteLoader,
               cursor: Cursor,
              ) -> None:
    print(f"Testing")

    original_records: Generator[Tuple[str, List[List[Any]]], None, None] = sqlite_loader.load_movies()

    for table_name, rows in original_records:
        normalized_data = normalize_data(table_name, rows)
        ids = [record.id for record in normalized_data]

        cursor.execute(
            f'SELECT * FROM content.{table_name} WHERE id = ANY(%s)',
            (ids,)
        )
        transferred_records = cursor.fetchall()

        model_class, columns_to_check = table_config.get(table_name)
        transferred_records = [model_class(**record) for record in transferred_records]


        assert len(normalized_data) == len(transferred_records),\
            f"Mismatch in number of records for {table_name}"

        trans_dict = {record.id: record for record in transferred_records}

        for original in normalized_data:
            trans = trans_dict.get(original.id)
            assert trans is not None, f"Record with ID {original.id} not found in PostgreSQL"

            for column in columns_to_check:
                original_value = getattr(original, column)
                trans_value = getattr(trans, column)
                assert original_value == trans_value, \
                    f"Mismatch in column '{column}' for record ID {original.id}"

        print(f"All records match for {table_name}. Data transfer successful!")