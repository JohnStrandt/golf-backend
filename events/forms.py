from django.forms import ModelForm, DateInput
from .models import Event, Match


class DateInput(DateInput):
    input_type = 'date'


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'format', 'date', 'course', 'side_played']
        widgets = {'date': DateInput()}    

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['opponent_1', 'opponent_2']
        
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
