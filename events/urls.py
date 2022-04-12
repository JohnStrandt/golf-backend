from django.urls import path
from . import views

urlpatterns = [
    path("", views.events, name="events"),
    path("matches/<str:pk>", views.matches, name="matches"),
    path("match/<str:pk>", views.match, name="match"),
    # path("nine-hole/<str:pk>", views.nineHole, name="nine-hole"),

    path("events-crud/", views.eventsCrud, name="events-crud"),
    path("create-event/", views.createEvent, name="create-event"),
    path("update-event/<str:pk>", views.updateEvent, name="update-event"),
    path("delete-event/<str:pk>", views.deleteEvent, name="delete-event"),

    path("matches-crud/<str:pk>", views.matchesCrud, name="matches-crud"),
    path("create-match/<str:pk>", views.createMatch, name="create-match"),
    path("update-match/<str:pk>", views.updateMatch, name="update-match"),
    path("delete-match/<str:pk>", views.deleteMatch, name="delete-match"),
]
