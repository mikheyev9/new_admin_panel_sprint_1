import os

LOCALE_PATHS = ['movies/locale']

SECRET_KEY = os.environ.get('SECRET_KEY', ''),

DEBUG = os.environ.get('DEBUG', False) == 'True'


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
INTERNAL_IPS = os.getenv('INTERNAL_IPS').split(',')

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'