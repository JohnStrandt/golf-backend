# Generated by Django 4.0 on 2022-01-13 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_course_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hole',
            options={'ordering': ['course', 'number']},
        ),
    ]