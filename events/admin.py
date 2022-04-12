from django.contrib import admin

from .models import Event, Match, PlayerScorecard, TeamScorecard

admin.site.register(Event)
admin.site.register(Match)
admin.site.register(PlayerScorecard)
admin.site.register(TeamScorecard)
