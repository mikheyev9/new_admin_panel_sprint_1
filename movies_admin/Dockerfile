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
    && poetry install --no-root --no-dev

# Копируем весь проект в контейнер
COPY . /app/

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    POETRY_VIRTUALENVS_CREATE=false

EXPOSE 8000

# Применяем миграции и запускаем сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
