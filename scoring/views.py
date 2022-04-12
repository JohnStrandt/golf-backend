from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from events.utils import calcMatchHDCP
from events.models import Player, TeamScorecard, PlayerScorecard
from course.models import Hole
from .selectors import searchMatches, nextMatch, makePlayerCard, makeTeamCard, getHoles


match = None
team_1 = None
team_2 = None
bench_1 = None
bench_2 = None

cards_1 = []
cards_2 = []
team_card_1 = None
team_card_2 = None

current_index = 0
num_holes = 0
holes = []


@login_required(login_url="login")
def setup(request):

    global match
    global team_1
    global team_2
    global bench_1
    global bench_2

    match = searchMatches(request)

    if match:
        if match.cards_made:
            return redirect("get-cards")

        else:
            team_1 = list(Player.objects.filter(team=match.opponent_1, is_sub=False))
            team_2 = list(Player.objects.filter(team=match.opponent_2, is_sub=False))
            bench_1 = list(Player.objects.filter(team=match.opponent_1, is_sub=True))
            bench_2 = list(Player.objects.filter(team=match.opponent_2, is_sub=True))

    else:
        return redirect("next-event")

    context = {"match": match, "team_1": team_1, "team_2": team_2}
    return render(request, "scoring/setup.html", context)


@login_required(login_url="login")
def choose_sub(request, pk):

    player = Player.objects.get(id=pk)

    if player.team == team_1[0].team:
        subs = bench_1

    else:
        subs = bench_2

    context = {"player": player, "subs": subs}
    return render(request, "scoring/choose_sub.html", context)


@login_required(login_url="login")
def sub_player(request, pk, sk):
    player = Player.objects.get(id=pk)
    sub = Player.objects.get(id=sk)
    global team_1
    global team_2
    global bench_1
    global bench_2

    if player in team_1:
        if team_1[0] == player:
            team_1[0] = sub
        else:
            team_1[1] = sub
        bench_1.remove(sub)
        bench_1.append(player)

    else:
        if team_2[0] == player:
            team_2[0] = sub
        else:
            team_2[1] = sub
        bench_2.remove(sub)
        bench_2.append(player)

    context = {"match": match, "team_1": team_1, "team_2": team_2}
    return render(request, "scoring/setup.html", context)


@login_required(login_url="login")
def show_teams(request):
    global match
    global team_1
    global team_2
    context = {"match": match, "team_1": team_1, "team_2": team_2}
    return render(request, "scoring/setup.html", context)


@login_required(login_url="login")
def next_event(request):
    match = nextMatch(request)
    context = {"match": match}
    return render(request, "scoring/next-event.html", context)


@login_required(login_url="login")
def get_cards(request):
    global match

    global team_1
    global team_2
    global cards_1
    global cards_2
    global team_card_1
    global team_card_2

    global num_holes
    global holes

    hdcp_1 = 0
    hdcp_2 = 0

    if match.cards_made:
        cards_1 = list(
            PlayerScorecard.objects.filter(match=match, team=match.opponent_1)
        )
        cards_2 = list(
            PlayerScorecard.objects.filter(match=match, team=match.opponent_2)
        )
        team_card_1 = TeamScorecard.objects.get(match=match, team=match.opponent_1)
        team_card_2 = TeamScorecard.objects.get(match=match, team=match.opponent_2)

    else:
        for player in team_1:
            hdcp_1 += player.handicap
            card = makePlayerCard(player, match)
            cards_1.append(card)

        for player in team_2:
            hdcp_2 += player.handicap
            card = makePlayerCard(player, match)
            cards_2.append(card)

        team_card_1 = makeTeamCard(match, match.opponent_1, hdcp_1)
        team_card_2 = makeTeamCard(match, match.opponent_2, hdcp_2)

        if not match.hdcp:
            match.hdcp = calcMatchHDCP(holes, team_card_1, team_card_2)

        match.cards_made = True
        match.save()

    if not holes:
        holes = list(getHoles(match.event))
        num_holes = len(holes)

    # return redirect("get-holes")
    return redirect("score-hole")


# @login_required(login_url="login")
# def get_holes(request):
#     global num_holes
#     global holes
#     global match

#     if not holes:
#         holes = list(getHoles(match.event))
#         num_holes = len(holes)

#     return redirect("score-hole")


@login_required(login_url="login")
def next_hole(request):
    global current_index
    global num_holes

    if current_index == num_holes - 1:
        current_index = 0
    else:
        current_index = current_index + 1

    return redirect("score-hole")


@login_required(login_url="login")
def prev_hole(request):
    global current_index
    global num_holes

    if current_index == 0:
        current_index = num_holes - 1
    else:
        current_index = current_index - 1

    return redirect("score-hole")


@login_required(login_url="login")
def score_hole(request):

    global match
    # global team_1
    # global team_2
    global holes
    global current_index
    global cards_1
    global cards_2
    # global team_card_1
    # global team_card_2

    print(holes[current_index].par)
    print(cards_1[0])

    temp_scores=[holes[current_index].par]*4
    index = 0

    print("type:")
    print(type(index))
    print(temp_scores)
    print("temp_scores[0]:")
    print(temp_scores[0])
    # hdcp is a dictionary
    hdcp_team = match.hdcp.get("team")
    strokes = match.hdcp.get("strokes_per_hole")[current_index]
    # par = holes[current_index].par

    # print(team_1)
    # print(team_2)
    # print(par)

    context = {
        "hole": holes[current_index],
        "match": match,
        "cards_1": cards_1,
        "cards_2": cards_2,
        "hdcp_team": hdcp_team,
        "strokes": strokes,
        "temp_scores": temp_scores,
        "index": index,
    }

    return render(request, "scoring/score_hole.html", context)


# print(player.user.get_full_name())

#     class TeamScorecard(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     handicap = models.PositiveSmallIntegerField(blank=True, null=True)
#     scores = models.JSONField(null=True, blank=True)
#     points = models.JSONField(null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(
#         default=uuid.uuid4, unique=True, primary_key=True, editable=False
#     )

# class PlayerScorecard(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
#     handicap = models.PositiveSmallIntegerField(blank=True, null=True)
#     scores = models.JSONField()
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(
#         default=uuid.uuid4, unique=True, primary_key=True, editable=False
#     )
