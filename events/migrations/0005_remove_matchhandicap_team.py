# Generated by Django 4.0 on 2022-04-29 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_playerscorecard_name_teamscorecard_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchhandicap',
            name='team',
        ),
    ]
