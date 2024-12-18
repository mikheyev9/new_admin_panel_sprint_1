import os

from config.settings import BASE_DIR

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'