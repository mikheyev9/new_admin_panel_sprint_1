-- Переключение на базу данных
\c movies_database

-- Создание схемы content
CREATE SCHEMA IF NOT EXISTS content;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
ALTER ROLE app SET search_path TO content, public;

-- Таблица film_work
CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    creation_date DATE,
    rating FLOAT CHECK (rating >= 0 AND rating <= 100),
    type VARCHAR(20) NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица genre
CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица person
CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Таблица genre_film_work
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id UUID PRIMARY KEY,
    genre_id UUID NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
    film_work_id UUID NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_genre_film_work UNIQUE (genre_id, film_work_id)

);

-- Таблица person_film_work
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY,
    person_id UUID NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
    film_work_id UUID NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL DEFAULT '',
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_person_film_role UNIQUE (person_id, film_work_id, role)
);

-- Индексы для таблицы film_work
CREATE INDEX IF NOT EXISTS idx_film_work_title ON content.film_work USING gin (title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_film_work_creation_date ON content.film_work (creation_date);

-- Индексы для таблицы person
CREATE INDEX IF NOT EXISTS idx_person_full_name ON content.person (full_name);

-- Индексы для таблицы genre_film_work
CREATE INDEX IF NOT EXISTS idx_genre_film_work_genre_id ON content.genre_film_work (genre_id);
CREATE INDEX IF NOT EXISTS idx_genre_film_work_id ON content.genre_film_work (film_work_id);

-- Индексы для таблицы person_film_work
CREATE INDEX IF NOT EXISTS idx_person_id_film_work_id ON content.person_film_work (person_id);
CREATE INDEX IF NOT EXISTS idx_person_film_work_id ON content.person_film_work (film_work_id);
