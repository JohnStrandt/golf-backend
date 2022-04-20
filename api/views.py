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
        # print("match_data: ",match_data.data)
        serializer = {"match": match_data.data, "rosters": roster_data}
        return Response(serializer)
    except:
        next_match = nextMatch()
        print("next_match: ",next_match)
        return Response(status=status.HTTP_404_NOT_FOUND)



# WAS GET
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def startResumeMatch(request, pk):
    hole_query = None
    pcards1_query = None
    pcards2_query = None

    try:
        # test this, should get todays match before coming here
        # returns match that user is playing in today
        # match = searchMatches(request)

        print(pk)
        print(request.data)
        match = Match.objects.get(id=pk)
        print(match)

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

            # for player in data["team1"]:
            #     temp = Player.objects.get(id=player["id"])
            #     team_1.append(temp)

            # for player in data["team2"]:
            #     temp = Player.objects.get(id=player["id"])
            #     team_2.append(temp)

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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updatePlayerScorecard(request, pk):
    card = PlayerScorecard.objects.get(id=pk)
    serializer = PlayerScorecardSerializer(instance=card, data=request.data)

    # could possibly update one hole here
    # hole = data.hole
    # card.scores['hole'] = data.score
    # PUT method?

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def updateTeamScorecard(request, pk):
    card = TeamScorecard.objects.get(id=pk)
    serializer = TeamScorecardSerializer(instance=card, data=request.data)

    print(card)

    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)
