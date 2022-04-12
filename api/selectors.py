from django.db.models import Q
from datetime import date
from events.models import Match, PlayerScorecard, TeamScorecard
from course.models import Hole
from league.models import Player



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


def getPlayerCard(player, match):
    obj, created = PlayerScorecard.objects.get_or_create(
        match=match,
        player=player,
        team=player.team,
        handicap=player.handicap,
    )
    return obj


def getTeamCard(match, team, handicap):
    obj, created = TeamScorecard.objects.get_or_create(
        match=match,
        team=team,
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


def getRosters(match):
    players_1 = Player.objects.filter(team=match.opponent_1, is_sub=False)
    players_2 = Player.objects.filter(team=match.opponent_2, is_sub=False)
    subs_1 = Player.objects.filter(team=match.opponent_1, is_sub=True)
    subs_2 = Player.objects.filter(team=match.opponent_2, is_sub=True)

    team1_id = str(match.opponent_1.id)
    team2_id = str(match.opponent_2.id)

    team1_name = match.opponent_1.name
    team2_name = match.opponent_2.name

    players1 = list()
    for player in players_1:
        players1.append({
            "name": player.user.get_full_name(), 
            "id": str(player.id)
            })

    players2 = list()
    for player in players_2:
        players2.append({
            "name": player.user.get_full_name(), 
            "id": str(player.id)
            })

    bench1 = None
    if subs_1:
        bench1 = list()
        for player in subs_1:
            bench1.append({
                "name": player.user.get_full_name(), 
                "id": str(player.id)
                })

    bench2 = None
    if subs_2:
        bench2 = list()
        for player in subs_2:
            bench2.append({
                "name": player.user.get_full_name(), 
                "id": str(player.id)
                })

    lineup = {
        "team1": { 
            "id": team1_id,
            "name": team1_name,
            "players": players1,
            "bench": bench1
            },
        "team2": { 
            "id": team2_id,
            "name": team2_name,
            "players": players2,
            "bench": bench2
        }
    }

    return lineup




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



def init_scores(side):
    first = 1
    last = 18
    if side == "Front":
        last = 9
    elif side == "Back":
        first = 10

    scores = {}
    for hole in range(first, last+1):
        scores[str(hole)] = 0

    return scores


def makePlayerCard(player, match):
    # side = match.event.side_played
    # scores = init_scores(side)
    # name = player.user.get_full_name()
    obj, created = PlayerScorecard.objects.get_or_create(
        match=match,
        player=player,
        team=player.team,
        handicap=player.handicap,
        # scores=scores
    )
    return obj


def makeTeamCard(match, team, handicap):
    side = match.event.side_played
    # scores = init_scores(side)
    obj, created = TeamScorecard.objects.get_or_create(
        match=match,
        team=team,
        handicap=handicap,
        # scores = scores
    )
    return obj

