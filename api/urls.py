from . import views
from django.urls import path
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path("", views.getRoutes),

    path("auth/login", MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/refreshtoken", TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.register, name='api_register'),

    path("league/", views.getLeague),

    path("players/", views.getPlayers),
    path("players/<str:pk>/", views.getPlayer),

    path("events/", views.getEvents),
    path("events/<str:pk>/", views.getEventMatches),

    path("match/", views.getTodaysMatch),
    path("match/next/", views.getNextMatch),
    path("match/<str:pk>/update-teams/", views.updateMatchTeams),
    path("match/<str:pk>/make-scorecards/", views.getScorecards),

    path("match/<str:pk>/score/", views.scoreHole),
    path("match/<str:pk>/bonus/", views.awardBonus),


    # not used yet
    path("player-cards/", views.getPlayerCards),
    path("team-cards/", views.getTeamCards),


    # testing url
    path("test/", views.test),
]

# RESTful naming convention (hopefully)