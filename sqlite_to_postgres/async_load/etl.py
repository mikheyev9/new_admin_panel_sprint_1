from typing import AsyncGenerator, List, Any
from dataclasses import astuple

import aiosqlite
import asyncpg

import async_load.models as models
from config import BATCH_SIZE


async def extract_data(sqlite_conn: aiosqlite.Connection,
                       table_name: str
                       ) -> AsyncGenerator[List[aiosqlite.Row], None]:
    query = f'SELECT * FROM {table_name}'

    async with sqlite_conn.execute(query) as cursor:
        while results := await cursor.fetchmany(BATCH_SIZE):
            yield results


async def transform_data(data: List[aiosqlite.Row],
                         table_name: str
                         ) -> List[Any]:
    match table_name:

        case 'film_work':
            return [models.FilmWork(
                id=item['id'],
                title=item['title'],
                description=item['description'] or '',
                creation_date=item['creation_date'],
                rating=item['rating'],
                type=item['type']
            ) for item in data]

        case 'genre':
            return [models.Genre(
                id=item['id'],
                name=item['name'],
                description=item['description'] or ''
            ) for item in data]

        case 'person':
            return [models.Person(
                id=item['id'],
                full_name=item['full_name']
            ) for item in data]

        case 'genre_film_work':
            return [models.GenreFilmwork(
                id=item['id'],
                film_work_id=item['film_work_id'],
                genre_id=item['genre_id']
            ) for item in data]

        case 'person_film_work':
            return [models.PersonFilmWork(
                id=item['id'],
                film_work_id=item['film_work_id'],
                person_id=item['person_id'],
                role=item['role']
            ) for item in data]

        case _:
            raise ValueError(f"Unknown table name: {table_name}")


async def load_data(pg_conn: asyncpg.Connection,
                    data: List[Any],
                    table_name: str
                     ) -> None:
    match table_name:

        case 'film_work':
            query = '''
            INSERT INTO content.film_work (id, title, description, creation_date, rating, type, created, modified)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description,
            creation_date = EXCLUDED.creation_date,
            rating = EXCLUDED.rating,
            type = EXCLUDED.type,
            modified = EXCLUDED.modified
            '''

        case 'genre':
            query = '''
            INSERT INTO content.genre (id, name, description, created, modified)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            modified = EXCLUDED.modified
            '''

        case 'person':
            query = '''
            INSERT INTO content.person (id, full_name, created, modified)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (id) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            modified = EXCLUDED.modified
            '''

        case 'genre_film_work':
            query = '''
            INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (film_work_id, genre_id) DO NOTHING
            '''

        case 'person_film_work':
            query = '''
            INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (film_work_id, person_id, role) DO NOTHING
            '''

        case _:
            raise ValueError(f"Unknown table: {table_name}")

    await pg_conn.executemany(query, [astuple(item) for item in data])
