from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from league.models import Player, Team, League
from events.models import Event, Match, TeamScorecard, PlayerScorecard
from course.models import Course, Hole



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def get_tokens(self, data):
        user = User.objects.get(username=data['username'])
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }



class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["name", "yards_out", "yards_in", "par_out", "par_in", "par_total"]


class HoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hole
        fields = ["number", "par", "handicap", "yardage", "image"]
        


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ["name", "id"]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name", "id"]


class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_player_name')
    team = serializers.SerializerMethodField('get_player_team')
    
    class Meta:
        model = Player
        fields = ["id", "name", "profile_image", "handicap", "team"]

    # serialized method field
    def get_player_name(self, player):
        username = player.user.get_full_name()
        return username
    
    def get_player_team(self, player):
        return player.team.name



class EventSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False)
    league = LeagueSerializer(many=False)
    class Meta:
        model = Event
        fields = ["id", "name", "date", "format", "side_played", "league", "course"]


class MatchSerializer(serializers.ModelSerializer):
    event = EventSerializer(many=False)
    
    class Meta:
        model = Match
        fields = ["id", "name", "current_hole", "event"]
        


class MatchStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Match
        fields = ["id", "cards_made", "name"]



# needed for initializing match info
class InitPlayerScorecardSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(many=False)
    class Meta:
        model = PlayerScorecard
        fields = ["player", "id", "handicap", "scores", "front", "back", "total"]


# needed for updating scorecard scores
class PlayerScorecardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerScorecard
        fields = ["id", "handicap", "scores", "front", "back", "total"]


class TeamScorecardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamScorecard
        fields = ["id", "handicap", "scores", "front", "back", "points"]





