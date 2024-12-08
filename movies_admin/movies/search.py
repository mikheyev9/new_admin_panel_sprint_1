from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q


def search_filmworks(queryset, query):
    search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
    search_query = SearchQuery(query)
    return queryset.annotate(
        rank=SearchRank(search_vector, search_query) +
             F('rating') / 100.0
    ).annotate(
        similarity=TrigramSimilarity('title', query) +
                   TrigramSimilarity('description', query)
    ).filter(
        Q(rank__gte=0.3) | Q(similarity__gte=0.3)
    ).order_by('-rank', '-similarity')