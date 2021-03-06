# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-17 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20170924_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='team',
            name='division',
            field=models.CharField(choices=[('O', 'Open'), ('X', 'Mixed'), ('W', 'Womens'), ('CO', 'College Open'), ('CW', 'College Open'), ('YO', 'Youth Open'), ('YX', 'Youth Mixed'), ('YW', 'Youth Womens')], max_length=20),
        ),
        migrations.AddField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(to='teams.Team'),
        ),
    ]
