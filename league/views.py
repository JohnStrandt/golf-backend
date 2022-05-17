from django.db.models.fields import NullBooleanField
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Player
from .forms import CustomUserCreationForm, PlayerForm
from .utils import searchProfiles, paginateProfiles



def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")
        #  may redirect elsewhere?  some other 'home' page??

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:  # user exists
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "my-profile")
        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, "league/login_register.html")


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # hold a temporary instance
            user.username = user.username.lower()
            user.save()  # user now officially added

            messages.success(request, "Profile was created!")

            login(request, user)
            return redirect("edit-profile")  # step 2 of 2 django create user??
        else:
            messages.error(request, "An error has occurred during registration...")

    context = {"page": page, "form": form}
    return render(request, "league/login_register.html", context)


@login_required(login_url="login")
def editProfile(request):
    player = request.user.player
    form = PlayerForm(instance=player)
    # pre-fills fields with current info

    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()

            return redirect("my-profile")

    context = {"form": form}
    return render(request, "league/player_form.html", context)


@login_required(login_url="login")
def myProfile(request):
    player = request.user.player
    context = {"player": player}
    return render(request, "league/my_profile.html", context)


# this was a dummy template, axe this??
def league(request, pk):
    msg = "Lakeside Golf League"
    context = {"message": msg}
    return render(request, "league/league.html", context)


def profiles(request):
    league = None
    if not (request.user.is_anonymous):
        league = request.user.player.league

    profiles, search_query = searchProfiles(request, league)

    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range, 'league': league}

    return render(request, 'league/profiles.html', context)


def userProfile(request, pk):
    profile = Player.objects.get(id=pk)
    context = {'profile': profile}
    return render(request, 'league/user_profile.html', context)
