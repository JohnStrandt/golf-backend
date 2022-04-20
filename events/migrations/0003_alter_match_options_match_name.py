# Generated by Django 4.0 on 2022-01-16 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_date_alter_event_format'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['event__league', 'event__date'], 'verbose_name_plural': 'matches'},
        ),
        migrations.AddField(
            model_name='match',
            name='name',
            field=models.CharField(blank=True, help_text='leave blank', max_length=50, null=True),
        ),
    ]