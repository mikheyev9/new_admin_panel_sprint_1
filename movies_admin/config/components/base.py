import os

LOCALE_PATHS = ['movies/locale']

SECRET_KEY = os.environ.get('SECRET_KEY', ''),

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['127.0.0.1']
INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'