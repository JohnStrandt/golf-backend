from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from league.models import Player
from events.models import Event, Match
from events.models import Match, PlayerScorecard, TeamScorecard

from .serializers import (
    EventSerializer,
    MatchSerializer,
    MatchStatusSerializer,
    InitPlayerScorecardSerializer,
    PlayerScorecardSerializer,
    PlayerSerializer,
    TeamScorecardSerializer,
    HoleSerializer,
    RegisterSerializer,
)

from .utils import calcMatchHDCP
from .selectors import (
    searchMatches,
    getRosters,
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
        {"GET": "/api/players/:player.id"},
        {"GET": "/api/events"},
        {"GET": "/api/events/:event.id"},
        {"GET": "/api/match"},
        {"GET": "/api/match/:match.id"},
        {"GET": "/api/cards/players"},
        {"GET": "/api/cards/teams"},
        {"POST": "/api/score/player"},
        {"POST": "/api/score/team"},
    ]

    return Response(routes)


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
    try:
        match = searchMatches(request)
        roster_data = getRosters(match)
        match_data = MatchStatusSerializer(match, many=False)
        serializer = {"match": match_data.data, "rosters": roster_data}
        return Response(serializer)
    except:
        next_match = nextMatch(request)
        print("next_match: ",next_match)
        return Response(next_match, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def startResumeMatch(request, pk):
    hole_query = None
    pcards1_query = None
    pcards2_query = None

    try:
        match = Match.objects.get(id=pk)

        if match.cards_made:
            pcards1_query = PlayerScorecard.objects.filter(
                match=match, team=match.opponent_1
            )
            player_cards_1 = list(pcards1_query)
            pcards2_query = PlayerScorecard.objects.filter(
                match=match, team=match.opponent_2
            )
            player_cards_2 = list(pcards2_query)

            team_card_1 = TeamScorecard.objects.get(match=match, team=match.opponent_1)
            team_card_2 = TeamScorecard.objects.get(match=match, team=match.opponent_2)

            hole_query = getHoles(match.event)

        else:
            data = request.data
            team_1 = []
            team_2 = []
            hdcp_1 = 0
            hdcp_2 = 0
            player_cards_1 = []
            player_cards_2 = []

            for playerID in data["team1"]:
                temp = Player.objects.get(id=playerID)
                team_1.append(temp)

            for playerID in data["team2"]:
                temp = Player.objects.get(id=playerID)
                team_2.append(temp)

            for player in team_1:
                hdcp_1 += player.handicap
                card = makePlayerCard(player, match)
                player_cards_1.append(card)

            for player in team_2:
                hdcp_2 += player.handicap
                card = makePlayerCard(player, match)
                player_cards_2.append(card)

            team_card_1 = makeTeamCard(match, match.opponent_1, hdcp_1)
            team_card_2 = makeTeamCard(match, match.opponent_2, hdcp_2)

            hole_query = getHoles(match.event)
            holes = list(hole_query)

            if not match.hdcp:
                match.hdcp = calcMatchHDCP(holes, team_card_1, team_card_2)

            match.cards_made = True
            match.save()

            pcards1_query = PlayerScorecard.objects.filter(
                match=match, team=match.opponent_1
            )
            pcards2_query = PlayerScorecard.objects.filter(
                match=match, team=match.opponent_2
            )

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    hole_serializer = HoleSerializer(hole_query, many=True)
    hole_data = dict()
    for hole in hole_serializer.data:
        hole_data.update({str(hole["number"]): hole})

    match_serializer = MatchSerializer(match, many=False)
    cards1_serializer = InitPlayerScorecardSerializer(pcards1_query, many=True)
    cards2_serializer = InitPlayerScorecardSerializer(pcards2_query, many=True)

    team1_card_serializer = TeamScorecardSerializer(team_card_1, many=False)
    team2_card_serializer = TeamScorecardSerializer(team_card_2, many=False)

    team1 = {
        "name": match.opponent_1.name,
        "id": match.opponent_1.id,
        "teamcard": team1_card_serializer.data,
        "playercards": cards1_serializer.data,
    }

    team2 = {
        "name": match.opponent_2.name,
        "id": match.opponent_2.id,
        "teamcard": team2_card_serializer.data,
        "playercards": cards2_serializer.data,
    }

    serializer = {
        "match": match_serializer.data,
        "holes": hole_data,
        "team1": team1,
        "team2": team2,
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
        if (side == "Front"):
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
        if (side == "Front"):
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





'''

                    NOT USED YET, BUT WORK NICELY

'''




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