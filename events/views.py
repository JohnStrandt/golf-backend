from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib import messages
from .selectors import getEvents, getHoles
from .models import Event, Match, PlayerScorecard, TeamScorecard, Player

from .forms import EventForm, MatchForm
from .utils import calcMatchHDCP


#       ===================================

#                   EVENTS

#       ===================================


@login_required(login_url="login")
def events(request):
    league = request.user.player.league
    events, search_query = getEvents(request, league)
    context = {"league": league, "events": events, "search_query": search_query}
    return render(request, "events/events.html", context)


@permission_required("is_staff", login_url="login")
def eventsCrud(request):
    league = request.user.player.league
    events, search_query = getEvents(request, league)
    context = {"league": league, "events": events, "search_query": search_query}
    return render(request, "events/events_crud.html", context)


@permission_required("is_staff", login_url="login")
def createEvent(request):
    form = EventForm()

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            # hold a temporary instance
            event.league = request.user.player.league
            event.name = event.name.lower()
            event.save()  # event now officially added
            messages.success(request, "Event was created!")
            return redirect("events-crud")

        else:
            messages.error(request, "An error has occurred")

    context = {"form": form}
    return render(request, "events/event_form.html", context)


@permission_required("is_staff", login_url="login")
def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)  # pre-fill fields

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event was updated successfully!")
            return redirect("events-crud")

    context = {"form": form, "event": event}
    return render(request, "events/update_event_form.html", context)


@permission_required("is_staff", login_url="login")
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    page = "events-crud"
    id_required = False

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event was deleted successfully!")
        return redirect("events-crud")

    context = {"object": event, "page": page, "id_required": id_required}
    return render(request, "delete_template.html", context)


#       ===================================

#                   MATCHES

#       ===================================


@login_required(login_url="login")
def matches(request, pk):
    event = Event.objects.get(id=pk)
    matches = Match.objects.filter(event=pk)
    context = {"event": event, "matches": matches}
    return render(request, "events/matches.html", context)


# may need to change to team_match
@login_required(login_url="login")
def match(request, pk):

    match = Match.objects.get(id=pk)
    holes = getHoles(request, match.event)

    try:
        team1_card = TeamScorecard.objects.get(match=pk, team=match.opponent_1)
        team2_card = TeamScorecard.objects.get(match=pk, team=match.opponent_2)

        team1_player_cards = PlayerScorecard.objects.filter(
            match=pk, team=match.opponent_1
        )
        team2_player_cards = PlayerScorecard.objects.filter(
            match=pk, team=match.opponent_2
        )

        if not match.hdcp:
            hdcp = calcMatchHDCP(holes, team1_card, team2_card)
            match.hdcp = hdcp
            match.save()

        context = {
            "match": match,
            "holes": holes,
            "team1_card": team1_card,
            "team2_card": team2_card,
            "team1_player_cards": team1_player_cards,
            "team2_player_cards": team2_player_cards,
        }

        if match.event.side_played != "Both":
            return render(request, "events/match.html", context)
        else:
            return render(request, "events/match.html", context)

    # if the match has not been played (no scorecards exist)
    except:
        return redirect("matches", match.event.id)


# @login_required(login_url="login")
# def match(request, pk):
#     match = Match.objects.get(id=pk)
#     print(match.event.side_played)
#     if match.event.side_played != "Both":
#         return redirect("nine-hole", pk)
#     else:
#         return redirect("nine-hole", pk)


@permission_required("is_staff", login_url="login")
def matchesCrud(request, pk):
    event = Event.objects.get(id=pk)
    matches = Match.objects.filter(event=pk)
    context = {"event": event, "matches": matches}
    return render(request, "events/matches_crud.html", context)


@permission_required("is_staff", login_url="login")
def createMatch(request, pk):
    form = MatchForm()
    event = Event.objects.get(id=pk)

    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            # hold a temporary instance
            match.event = event
            match.save()  # match added
            messages.success(request, "Match was created!")
            return redirect("matches-crud", event.id)

        else:
            messages.error(request, "An error has occurred")

    context = {"form": form, "event": event}
    return render(request, "events/match_form.html", context)


@permission_required("is_staff", login_url="login")
def updateMatch(request, pk):
    match = Match.objects.get(id=pk)
    form = MatchForm(instance=match)  # pre-fill fields

    if request.method == "POST":
        form = MatchForm(request.POST, request.FILES, instance=match)
        if form.is_valid():
            form.save()
            messages.success(request, "Match was updated successfully!")
            return redirect("matches-crud", match.event.id)

    context = {"form": form, "match": match}
    return render(request, "events/update_match_form.html", context)


@permission_required("is_staff", login_url="login")
def deleteMatch(request, pk):
    match = Match.objects.get(id=pk)
    page = "matches-crud"
    id_required = True

    if request.method == "POST":
        match.delete()
        messages.success(request, "Match was deleted successfully!")
        return redirect("matches-crud", match.event.id)

    context = {"object": match, "page": page, "id_required": id_required}
    return render(request, "delete_template.html", context)
