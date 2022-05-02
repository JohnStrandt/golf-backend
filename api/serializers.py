from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from league.models import Player, Team, League
from events.models import Event, Match, TeamScorecard, PlayerScorecard, MatchHandicap
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
    team1_name = serializers.SerializerMethodField('get_team1_name')
    team2_name = serializers.SerializerMethodField('get_team2_name')

    class Meta:
        model = Match
        fields = ["id", "name", "current_hole", "team1", "team2", "team1_name", "team2_name","event", "cards_made"]
    
    def get_team1_name(self, match):
        return match.opponent_1.name

    def get_team2_name(self, match):
        return match.opponent_2.name



class PlayerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["profile_image"]



class PlayerScorecardSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField('get_player_photo')
    class Meta:
        model = PlayerScorecard
        fields = ["id", "name", "profile_image", "handicap", "scores", "front", "back", "total"]
    
    def get_player_photo(self, scorecard):
        photo = PlayerPhotoSerializer(scorecard.player, many=False)
        return photo.data["profile_image"]


class TeamScorecardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamScorecard
        fields = ["id", "name", "handicap", "scores", "front", "back", "points"]


class MatchHandicapSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchHandicap
        fields = '__all__'
