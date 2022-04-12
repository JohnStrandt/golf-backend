from django.db.models import Q
from datetime import date
from events.models import Match, PlayerScorecard, TeamScorecard
from course.models import Hole


def searchMatches(request):
    today = date.today()
    team = request.user.player.team
    try:
        match = Match.objects.distinct().get(
            Q(event__date__iexact=today) & (Q(opponent_1=team) | Q(opponent_2=team))
        )
    except:
        match = None

    return match


def nextMatch(request):
    today = date.today()
    team = request.user.player.team
    try:
        match = (
            Match.objects.distinct()
            .filter(
                Q(event__date__gt=today) & (Q(opponent_1=team) | Q(opponent_2=team))
            )
            .order_by("event__date")[0]
        )
    except:
        match = None

    return match


def makePlayerCard(player, match):
    obj, created = PlayerScorecard.objects.get_or_create(
        match=match,
        player=player,
        team=player.team,
        handicap=player.handicap,
    )
    return obj


def makeTeamCard(match, team, handicap):
    obj, created = TeamScorecard.objects.get_or_create(
        match=match,
        team=team,
        handicap=handicap,
    )
    return obj


def getHoles(event):

    first = 1
    last = 18

    if event.course.is_nine or event.side_played == "Front":
        last = 9
    elif event.side_played == "Back":
        first = 10

    try:
        holes = (
            Hole.objects.distinct()
            .filter(Q(course=event.course) & Q(number__gte=first) & Q(number__lte=last))
            .order_by("number")
        )
    except:
        holes = None

    return holes


#  from events/selectors.py
# def getHoles(request, event):
# start = 1
# end = 18
# if (event.side_played == 'Front'):
#     end = 9
# elif(event.side_played == 'Back'):
#     start = 10

# holes = Hole.objects.distinct().filter(
#     Q(course=event.course) &
#     Q(number__range=(start, end))
# )
# return holes
