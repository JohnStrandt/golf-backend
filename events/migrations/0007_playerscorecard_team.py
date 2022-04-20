# Generated by Django 4.0 on 2022-02-02 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0012_alter_team_options'),
        ('events', '0006_teamscorecard_handicap'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerscorecard',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='league.team'),
        ),
    ]