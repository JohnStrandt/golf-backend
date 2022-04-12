from django.db import models
from django.db.models.fields import BooleanField
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

from django.utils.text import slugify
from .utils import PAR_CHOICES, STATE_CHOICES


class Club(models.Model):
    name = models.CharField(max_length=150,  help_text="Formal name for the golf course (ex: Augusta National Golf Course)")
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip = models.CharField(max_length=12, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    has_multiple_courses = BooleanField(
        default=False, help_text="Check here if the club has more than one course."
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Course(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=25,
        help_text='If the club has just one course, use a simple version of the club\'s formal name (example: Augusta National Golf Course would be "Augusta")'
    )
    yards_out = models.PositiveSmallIntegerField(help_text="Front nine total yards.")
    par_out = models.PositiveSmallIntegerField(help_text="Front nine par total.")
    yards_in = models.PositiveSmallIntegerField(help_text="Back nine total yards.")
    par_in = models.PositiveSmallIntegerField(help_text="Back nine par total.")
    yards_total = models.PositiveSmallIntegerField(help_text="Front + Back total yards")
    par_total = models.PositiveSmallIntegerField(help_text="Front + Back par")
    is_nine = BooleanField(
        default=False, help_text="Check here if this course is a nine-hole course."
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        state = self.club.state
        club = self.club.name
        course = self.name
        return f"{state}, {club}, {course}"

    class Meta:
        ordering = ['name']


def create_path(instance, filename):
    state = instance.course.club.state.lower()
    club = slugify(instance.course.club.name.lower())
    course = slugify(instance.course.name.lower())
    path = f"courses/{state}/{club}/{course}/{filename}"
    print(path)
    return path


class Hole(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(18), MinValueValidator(1)])
    par = models.PositiveSmallIntegerField(choices=PAR_CHOICES)
    handicap = models.PositiveSmallIntegerField(validators=[MaxValueValidator(18), MinValueValidator(1)])
    yardage = models.PositiveSmallIntegerField()
    image = models.ImageField(null=True, blank=True, upload_to=create_path)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        state = self.course.club.state
        club = self.course.club.name
        course = self.course.name
        number = self.number
        return f"{state} - {club}, {course} {number}"

    class Meta:
        ordering = ['course', 'number']

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url = ''
        return url