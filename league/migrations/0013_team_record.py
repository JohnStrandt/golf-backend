# Generated by Django 4.0 on 2022-03-03 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0012_alter_team_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='record',
            field=models.JSONField(blank=True, help_text='leave blank', null=True),
        ),
    ]