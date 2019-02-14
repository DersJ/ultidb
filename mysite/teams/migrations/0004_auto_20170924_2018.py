# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20170924_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='division',
            field=models.CharField(choices=[('OPEN', 'Open'), ('MIXED', 'Mixed'), ('WOMENS', 'Womens'), ('COLLEGEOPEN', 'College Open'), ('COLLEGEWOMENS', 'College Open'), ('YOUTHOPEN', 'Youth Open'), ('YOUTHMIXED', 'Youth Mixed'), ('YOUTHWOMENS', 'Youth Womens')], max_length=20),
        ),
    ]
