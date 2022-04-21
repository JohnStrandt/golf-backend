from django.contrib import admin

from .models import Event, Match, PlayerScorecard, TeamScorecard, MatchHandicap

admin.site.register(Event)
admin.site.register(Match)
admin.site.register(PlayerScorecard)
admin.site.register(TeamScorecard)
admin.site.register(MatchHandicap)
