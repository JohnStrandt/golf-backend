# Generated by Django 4.0 on 2022-01-02 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0003_remove_player_email_remove_player_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
