from django.urls import path
from . import views

urlpatterns = [
  path('', views.setup, name='setup'),
  path('next-event', views.next_event, name='next-event'),
  path('choose-sub/<str:pk>', views.choose_sub, name='choose-sub'),
  path('sub-player/<str:pk>, <str:sk>', views.sub_player, name='sub-player'),
  path('show-teams/', views.show_teams, name='show-teams'),

  path('get-cards/', views.get_cards, name='get-cards'),
  # path('get-holes/', views.get_holes, name='get-holes'),
  path('score-hole/', views.score_hole, name='score-hole'),

  path('prev-hole/', views.prev_hole, name='prev-hole'),
  path('next-hole/', views.next_hole, name='next-hole'),
]