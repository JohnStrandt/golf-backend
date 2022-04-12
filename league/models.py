from django.db import models
from django.contrib.auth.models import User
from course.models import Club
import uuid
from django.utils.text import slugify


class League(models.Model):
    name = models.CharField(max_length=150, unique=True)
    club = models.ForeignKey(Club, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name


class Team(models.Model):
    league = models.ForeignKey(League, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    record = models.JSONField(blank=True, default=dict)
    points = models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-name"]


def create_path(instance, filename):
    if instance.league:
        league = slugify(instance.league.name.lower())
    else:
        league = "default"
    path = f"profiles/{league}/{filename}"
    print(path)
    return path


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=create_path,
        default="profiles/user-default.png",
    )

    league = models.ForeignKey(League, blank=True, null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.SET_NULL)
    handicap = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    is_sub = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['-team']

    @property
    def imageURL(self):
        try:
            url=self.profile_image.url
        except:
            url = ''
        return url
        # this prevents crash if no image exists
