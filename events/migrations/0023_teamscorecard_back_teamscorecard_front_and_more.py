# Generated by Django 4.0 on 2022-03-09 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_alter_teamscorecard_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamscorecard',
            name='back',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='teamscorecard',
            name='front',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='teamscorecard',
            name='scores',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]