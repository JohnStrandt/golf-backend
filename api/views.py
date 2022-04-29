from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from league.models import Player
from events.models import Event, Match, MatchHandicap, PlayerScorecard, TeamScorecard


from .serializers import (
    RegisterSerializer,
    LeagueSerializer,
    EventSerializer,
    MatchSerializer,
    HoleSerializer,
    PlayerSerializer,
    PlayerScorecardSerializer,
    TeamScorecardSerializer,
    MatchHandicapSerializer,
)

from .utils import calcMatchHDCP
from .selectors import (
    searchMatches,
    makePlayerCard,
    makeTeamCard,
    getHoles,
    nextMatch,
)


# login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # custom claim
        token["username"] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def register(request):
    data = request.data
    password = make_password(data["password"])
    serializer = RegisterSerializer(data=data, many=False)

    if serializer.is_valid():
        serializer.save(password=password)
        tokens = serializer.get_tokens(data)

        return Response(tokens, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"POST": "/api/login"},
        {"POST": "/api/signin"},
        {"POST": "/api/register"},
        {"GET": "/api/players"},
        {"GET": "/api/players/:player_id"},
        {"GET": "/api/events"},
        {"GET": "/api/events/:event_id"},
        {"GET": "/api/match"},
        {"GET": "/api/match/:match_id"},
        {"GET": "/api/cards/players"},
        {"GET": "/api/cards/teams"},
        {"POST": "/api/score/player"},
        {"POST": "/api/score/team"},
    ]

    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getLeague(request):
    league = request.user.player.league
    serializer = LeagueSerializer(league, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getPlayers(request):
    league = request.user.player.league
    players = Player.objects.filter(league=league)
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getPlayer(request, pk):
    player = Player.objects.get(id=pk)
    serializer = PlayerSerializer(player, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getEvents(request):
    league = request.user.player.league
    events = Event.objects.filter(league=league)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getEventMatches(request, pk):
    matches = Match.objects.filter(event=pk)
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTodaysMatch(request):

    match = searchMatches(request)
    holes = getHoles(match.event)
    players1_query = Player.objects.filter(team=match.opponent_1, is_sub=False)
    players2_query = Player.objects.filter(team=match.opponent_2, is_sub=False)
    subs1_query = Player.objects.filter(team=match.opponent_1, is_sub=True)
    subs2_query = Player.objects.filter(team=match.opponent_2, is_sub=True)

    match_serializer = MatchSerializer(match, many=False)
    hole_serializer = HoleSerializer(holes, many=True)
    players1_serializer = PlayerSerializer(players1_query, many=True)
    players2_serializer = PlayerSerializer(players2_query, many=True)
    subs1_serializer = PlayerSerializer(subs1_query, many=True)
    subs2_serializer=PlayerSerializer(subs2_query, many=True)

    serializer = {
        "match": match_serializer.data,
        "holes": hole_serializer.data,
        "starters1": players1_serializer.data,
        "starters2": players2_serializer.data,
        "subs1": subs1_serializer.data,
        "subs2": subs2_serializer.data,
        }

    return Response(serializer)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updateMatchTeams(request, pk):

    match = Match.objects.get(id=pk)
    data = request.data

    match.team1 = data["team1"]
    match.team2 = data["team2"]
    match.save()

    serializer = MatchSerializer(match, many=False)

    return Response(serializer.data, status = status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getScorecards(request, pk):

    match = Match.objects.get(id=pk)
    data = request.data
    scorecards1 = []
    scorecards2 = []
    hdcp1 = 0
    hdcp2 = 0

    for playerID in data["team1"]:
        player = Player.objects.get(id=playerID)
        hdcp1 += player.handicap
        card = makePlayerCard(player, match)
        scorecards1.append(card)

    for playerID in data["team2"]:
        player = Player.objects.get(id=playerID)
        hdcp2 += player.handicap
        card = makePlayerCard(player, match)
        scorecards2.append(card)

    teamCard1 = makeTeamCard(match, match.opponent_1, hdcp1)
    teamCard2 = makeTeamCard(match, match.opponent_2, hdcp2)

    hole_query = getHoles(match.event)
    holes = list(hole_query)

    handicap = calcMatchHDCP(holes, teamCard1, teamCard2)
    match_hdcp, created = MatchHandicap.objects.get_or_create(match=match, hdcp=handicap)
    match_hdcp.save()

    if not match.cards_made:
        match.cards_made = True
        match.save()

    playerSerializer1 = PlayerScorecardSerializer(scorecards1, many=True)
    playerSerializer2 = PlayerScorecardSerializer(scorecards2, many=True)
    teamSerializer1 = TeamScorecardSerializer(teamCard1, many=False)
    teamSerializer2 = TeamScorecardSerializer(teamCard2, many=False)
    hdcpSerializer = MatchHandicapSerializer(match_hdcp, many=False)

    serializer = {
        "handicap": hdcpSerializer.data,
        "cards1": {
            "team": teamSerializer1.data,
            "players": playerSerializer1.data
        },
        "cards2": {
            "team": teamSerializer2.data,
            "players": playerSerializer2.data
        }
    }

    return Response(serializer)


def add_scores(scores):
    total = 0
    for value in scores.values():
        if not value == None:
            total += value
    return total


def update_team_cards(cards, hole, side):
    for _card in cards:
        card = TeamScorecard.objects.get(id=_card["id"])
        card.scores.update({str(hole): _card["score"]})

        total = add_scores(card.scores)
        if side == "Front":
            card.front = total
        else:
            card.back = total
        card.points = total

        card.save()


def update_player_cards(cards, hole, side):
    for _card in cards:
        card = PlayerScorecard.objects.get(id=_card["id"])
        card.scores.update({str(hole): _card["score"]})

        total = add_scores(card.scores)
        if side == "Front":
            card.front = total
        else:
            card.back = total
        card.total = total

        card.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def scoreHole(request):
    data = request.data
    hole = data["hole"]
    side = data["side"]
    teamCards = data["team_cards"]
    playerCards = data["player_cards"]

    update_team_cards(teamCards, hole, side)
    update_player_cards(playerCards, hole, side)

    message = "Cards Updated"
    return Response(message)



"""

                    NOT USED YET, BUT WORKS NICELY

"""

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getPlayerCards(request):
    match = searchMatches(request)
    cards = PlayerScorecard.objects.filter(match=match)
    serializer = PlayerScorecardSerializer(cards, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getTeamCards(request):
    match = searchMatches(request)
    cards = TeamScorecard.objects.filter(match=match)
    serializer = TeamScorecardSerializer(cards, many=True)
    return Response(serializer.data)


#               TESTING


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def test(request):
    data = request.data
    lunch = data["lunch"]

    print(lunch)

    return Response("Testing Done")
