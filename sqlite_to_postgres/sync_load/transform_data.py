from typing import Generator, Tuple, List, Any

import sync_load.models as models


def normalize_data(table_name: str,
                   data: List[Any]) -> List[Any]:
    match table_name:
        case 'film_work':
            return [models.FilmWork(
                id=item['id'],
                title=item['title'],
                description=item['description'] or '',
                creation_date=item['creation_date'],
                rating=item['rating'],
                type=item['type'] or '',
            ) for item in data]

        case 'genre':
            return [models.Genre(
                id=item['id'],
                name=item['name'],
                description=item['description'] or '',
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
            raise ValueError(f"Unknown table: {table_name}")