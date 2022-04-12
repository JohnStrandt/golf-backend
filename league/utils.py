from django.db.models import Q
from .models import Player
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    page = request.GET.get("page")
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, profiles


def searchProfiles(request, league):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    # __iexact - must match perfectly
    # __icontains - search with partial words
    # distinct() eliminates duplicates
    profiles = Player.objects.distinct().filter(
        Q(league__name__iexact=league)
        & (
            Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(team__name__icontains=search_query)
        )
    )

    return profiles, search_query
