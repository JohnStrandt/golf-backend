from django.forms import ModelForm
from events.models import TeamScorecard, PlayerScorecard


class ScorecardSetupForm(ModelForm):
    class Meta:
        model = TeamScorecard
        fields = ['match', 'team', 'handicap'] 

    def __init__(self, *args, **kwargs):
        super(ScorecardSetupForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


# class TeamScorecard(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     handicap = models.PositiveSmallIntegerField(blank=True, null=True)
#     scores = models.JSONField(null=True, blank=True)
#     points = models.JSONField(null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(
#         default=uuid.uuid4, unique=True, primary_key=True, editable=False
#     )