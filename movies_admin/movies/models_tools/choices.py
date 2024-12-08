from django.db import models
from django.utils.translation import gettext_lazy as _


class FilmType(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    TV_SHOW = 'tv_show', _('TV Show')
