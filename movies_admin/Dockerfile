# Указываем базовый образ
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev \
    && poetry cache clear pypi --all -n

# Копируем весь проект в контейнер
COPY . /app/

EXPOSE 8000