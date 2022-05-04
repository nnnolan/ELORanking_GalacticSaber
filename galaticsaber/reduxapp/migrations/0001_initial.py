# Generated by Django 4.0.2 on 2022-05-04 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LSDGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1', models.CharField(max_length=20)),
                ('player2', models.CharField(max_length=20)),
                ('result', models.FloatField()),
                ('player2ELO', models.IntegerField()),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MTGGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1', models.CharField(max_length=20)),
                ('player2', models.CharField(max_length=20)),
                ('result', models.FloatField()),
                ('player1ELO', models.IntegerField()),
                ('player2ELO', models.IntegerField()),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realname', models.CharField(blank=True, max_length=20)),
                ('mtg_currentELO', models.IntegerField(default=1000)),
                ('mtg_highestELO', models.IntegerField(default=1000)),
                ('mtg_lowestELO', models.IntegerField(default=1000)),
                ('lsd_currentELO', models.IntegerField(default=1000)),
                ('lsd_highestELO', models.IntegerField(default=1000)),
                ('lsd_lowestELO', models.IntegerField(default=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
