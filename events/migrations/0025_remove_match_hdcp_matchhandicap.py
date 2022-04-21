# Generated by Django 4.0 on 2022-04-21 18:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0016_remove_team_pints'),
        ('events', '0024_alter_playerscorecard_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='hdcp',
        ),
        migrations.CreateModel(
            name='MatchHandicap',
            fields=[
                ('hdcp', models.JSONField(blank=True, default=dict, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.team')),
            ],
        ),
    ]
