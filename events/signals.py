from django.db.models.signals import post_save
from .models import Match, TeamScorecard
from league.models import Team

# So far, not used

# team record tuples, points re-calculated on update
# Update Team points just once... tuples?