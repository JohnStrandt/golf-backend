# Generated by Django 4.0 on 2022-02-18 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_alter_playerscorecard_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='side_played',
            field=models.CharField(choices=[('Front', 'Front'), ('Back', 'Back'), ('Both', 'Both')], max_length=5),
        ),
    ]