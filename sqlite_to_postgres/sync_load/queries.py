SQL_QUERIES = {
    'film_work': '''
        INSERT INTO content.film_work (id, title, description, creation_date, rating, type, created, modified)
        VALUES (%(id)s, %(title)s, %(description)s, %(creation_date)s, %(rating)s, %(type)s, %(created)s, %(modified)s)
        ON CONFLICT (id) DO UPDATE SET
        title = EXCLUDED.title,
        description = EXCLUDED.description,
        creation_date = EXCLUDED.creation_date,
        rating = EXCLUDED.rating,
        type = EXCLUDED.type,
        modified = EXCLUDED.modified
    ''',
    'genre': '''
        INSERT INTO content.genre (id, name, description, created, modified)
        VALUES (%(id)s, %(name)s, %(description)s, %(created)s, %(modified)s)
        ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        description = EXCLUDED.description,
        modified = EXCLUDED.modified
    ''',
    'person': '''
        INSERT INTO content.person (id, full_name, created, modified)
        VALUES (%(id)s, %(full_name)s, %(created)s, %(modified)s)
        ON CONFLICT (id) DO UPDATE SET
        full_name = EXCLUDED.full_name,
        modified = EXCLUDED.modified
    ''',
    'genre_film_work': '''
        INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created)
        VALUES (%(id)s, %(film_work_id)s, %(genre_id)s, %(created)s)
        ON CONFLICT (film_work_id, genre_id) DO NOTHING
    ''',
    'person_film_work': '''
        INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created)
        VALUES (%(id)s, %(film_work_id)s, %(person_id)s, %(role)s, %(created)s)
        ON CONFLICT (film_work_id, person_id, role) DO NOTHING
    ''',
}
