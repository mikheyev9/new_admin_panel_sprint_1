import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.indexes import GinIndex

from movies.models_tools.choices import FilmType
from movies.models_tools.validators import RATING_VALIDATORS


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(verbose_name=_("Created"), editable=False)
    modified = models.DateTimeField(verbose_name=_("Modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, default='')
    film_works = models.ManyToManyField('FilmWork', through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        indexes = [
            models.Index(fields=['name'], name='idx_genre_name'),
        ]

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('Full name'), max_length=100)
    film_works = models.ManyToManyField('FilmWork', through='PersonFilmWork')

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        indexes = [
            models.Index(fields=['full_name'], name='idx_person_full_name')
        ]

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(verbose_name=_("Title"), max_length=255, blank=False, null=False)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=False)
    creation_date = models.DateField(verbose_name=_("Creation Date"), blank=True, null=True)
    rating = models.FloatField(
        verbose_name=_("Rating"),
        validators=RATING_VALIDATORS,
        blank=True,
        null=True
    )
    type = models.CharField(
        verbose_name=_("Type"),
        max_length=20,
        choices=FilmType.choices,
        blank=False,
        null=False
    )
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmWork')


    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _("Film Work")
        verbose_name_plural = _("Film Works")
        indexes = [
            GinIndex(fields=['title'], name='idx_film_work_title', opclasses=['gin_trgm_ops']),
            models.Index(fields=['creation_date'], name='idx_film_work_creation_date'),
        ]

    def __str__(self):
        return self.title



class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE, verbose_name=_('Film Work'))
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, verbose_name=_('Genre'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='unique_genre_film_work')
        ]
        indexes = [
            models.Index(fields=['film_work'], name='idx_genre_film_work_id'),
            models.Index(fields=['genre'], name='idx_genre_film_work_genre_id'),
        ]

    def __str__(self):
        return f'{self.genre.name} for "{self.film_work.title}"'


class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, verbose_name=_('Person'))
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE, verbose_name=_('Film'))
    role = models.CharField(_('Role'), max_length=100, null=False, default='')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person Film Work')
        verbose_name_plural = _('Person Film Works')
        constraints = [
            models.UniqueConstraint(fields=['person', 'film_work', 'role'], name='unique_person_film_role')
        ]
        indexes = [
            models.Index(fields=['person'], name='idx_person_id_film_work_id'),
            models.Index(fields=['film_work'], name='idx_person_film_work_id'),
        ]

    def __str__(self):
        return f"{self.person.full_name} - {self.film_work.title} ({self.role})"