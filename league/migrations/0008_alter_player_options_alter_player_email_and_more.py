# Generated by Django 4.0 on 2022-01-06 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0007_alter_player_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['-team']},
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
