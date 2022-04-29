from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from course.models import Course
from .utils import SIDE_CHOICES, FORMAT_CHOICES
from league.models import League, Team, Player
import uuid


class Event(models.Model):
    name = models.CharField(max_length=150, help_text="Event Name ex: week 5")
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    date = models.DateField()
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    side_played = models.CharField(max_length=5, choices=SIDE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        league = self.league
        name = self.name
        date = self.date
        return f"{league}: {name} {date}"

    class Meta:
        ordering = ["-created"]


class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    opponent_1 = models.ForeignKey(Team, related_name='home', null=True, on_delete=models.CASCADE)
    opponent_2 = models.ForeignKey(Team, related_name='away', null=True, on_delete=models.CASCADE)
    team1 = ArrayField(models.UUIDField(), null=True, blank=True, help_text="leave blank")
    team2 = ArrayField(models.UUIDField(), null=True, blank=True, help_text="leave blank")
    name = models.CharField(max_length=50, null=True, blank=True, help_text="leave blank")
    cards_made = models.BooleanField(default=False)
    current_hole = models.PositiveSmallIntegerField(default=0)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def save(self, *args, **kwargs):
        self.name = f'{self.opponent_1.name} vs {self.opponent_2.name}'
        super().save(*args, **kwargs)

    def __str__(self):
        league = self.event.league.name
        event = self.event.name
        name = self.name
        return f"{league}, {event}: {name}"

    class Meta:
        verbose_name_plural = "matches"
        ordering = ["event__league", "event__date"]



class MatchHandicap(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    hdcp = models.JSONField(null=True, blank=True, default=dict)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        event = self.match.event.name
        match = self.match.name
        return f"{event}: {match}"

    class Meta:
        ordering = ["match__event__league", "created"]



class TeamScorecard(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=25, blank=True, null=True)
    handicap = models.PositiveSmallIntegerField(blank=True, null=True)
    scores = models.JSONField(null=True, blank=True, default=dict)
    front = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    back = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    points = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def save(self, *args, **kwargs):
        self.name = self.team.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.match.event.name}"

    class Meta:
        ordering = ["created"]


class PlayerScorecard(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=25, blank=True, null=True)
    handicap = models.PositiveSmallIntegerField(blank=True, null=True)
    scores = models.JSONField(blank=True, null=True, default=dict)
    front = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    back = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    total = models.PositiveSmallIntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def save(self, *args, **kwargs):
        self.handicap = self.player.handicap
        self.team = self.player.team # may not need this
        self.name = self.player.user.get_full_name()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.match.event.name}"

    class Meta:
        ordering = ["created"]