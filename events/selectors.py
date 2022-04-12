from django.db.models import Q
from .models import Event
from course.models import Hole


def getEvents(request, league):
    search_query = ""
    # search_query not used so far
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    events = Event.objects.distinct().filter(
        Q(league__name__iexact=league)
    )
    return events, search_query

# I think there is another in scoring
def getHoles(request, event):
    start = 1
    end = 18
    if (event.side_played == 'Front'):
        end = 9
    elif(event.side_played == 'Back'):
        start = 10
    
    holes = Hole.objects.distinct().filter(
        Q(course=event.course) &
        Q(number__range=(start, end))
    )
    return holes
