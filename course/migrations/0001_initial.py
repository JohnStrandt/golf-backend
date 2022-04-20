# Generated by Django 4.0 on 2022-01-10 22:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='address')),
                ('city', models.CharField(blank=True, max_length=150, null=True, verbose_name='city')),
                ('state', models.CharField(blank=True, max_length=150, null=True, verbose_name='state')),
                ('zip', models.CharField(blank=True, max_length=12, null=True, verbose_name='zip')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('is_nine', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('club', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.club')),
            ],
        ),
        migrations.CreateModel(
            name='Hole',
            fields=[
                ('number', models.CharField(max_length=150)),
                ('par', models.PositiveSmallIntegerField(choices=[(3, '3'), (4, '4'), (5, '5')])),
                ('handicap', models.PositiveSmallIntegerField()),
                ('yardage', models.PositiveSmallIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='courses/{{course.name}}/')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course')),
            ],
        ),
    ]