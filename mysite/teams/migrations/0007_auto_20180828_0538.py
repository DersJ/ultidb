# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-28 05:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0006_auto_20180817_0737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team0_score', models.IntegerField(default=0)),
                ('team1_score', models.IntegerField(default=0)),
                ('date_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RosterMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games', models.ManyToManyField(to='teams.Game')),
                ('teams', models.ManyToManyField(to='teams.Team')),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='rosters',
        ),
        migrations.AddField(
            model_name='rostermembership',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='teams.Player'),
        ),
        migrations.AddField(
            model_name='rostermembership',
            name='roster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='teams.Roster'),
        ),
        migrations.AddField(
            model_name='roster',
            name='games',
            field=models.ManyToManyField(blank=True, related_name='games', to='teams.Game'),
        ),
        migrations.AddField(
            model_name='roster',
            name='players',
            field=models.ManyToManyField(through='teams.RosterMembership', to='teams.Player'),
        ),
    ]
