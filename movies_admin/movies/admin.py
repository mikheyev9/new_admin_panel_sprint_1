from django.contrib import admin, messages

from django.db.models import Value, FloatField

from movies import models
from movies.search import search_filmworks


class GenreFilmworkInline(admin.TabularInline):
    model = models.GenreFilmwork
    extra = 1

class PersonFilmworkInline(admin.TabularInline):
    model = models.PersonFilmWork
    extra = 1


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    search_fields = ('name',)
    list_display = ('name', 'description')
    list_per_page = 50


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)
    search_fields = ('full_name',)
    list_display = ('full_name',)
    list_per_page = 50
    show_full_result_count = True


@admin.register(models.FilmWork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_rank', 'get_similarity')
    list_filter = ('type',)
    search_fields = ('title', 'description')
    list_per_page = 50
    show_full_result_count = True
    actions = ['delete_all_films']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            rank=Value(0.0, output_field=FloatField()),
            similarity=Value(0.0, output_field=FloatField())
        )
        return queryset

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            queryset = search_filmworks(queryset, search_term)
        return queryset, False

    def get_rank(self, obj):
        return round(obj.rank, 2) if hasattr(obj, 'rank') else '-'
    get_rank.admin_order_field = 'rank'
    get_rank.short_description = 'Rank'

    def get_similarity(self, obj):
        return round(obj.similarity, 2) if hasattr(obj, 'similarity') else '-'
    get_similarity.admin_order_field = 'similarity'
    get_similarity.short_description = 'Similarity'
