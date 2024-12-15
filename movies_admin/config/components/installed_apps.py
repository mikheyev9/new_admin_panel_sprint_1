from config.components.base import DEBUG

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'movies.apps.MoviesConfig',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')