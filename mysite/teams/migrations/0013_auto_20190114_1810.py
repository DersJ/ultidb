# Generated by Django 2.1.5 on 2019-01-14 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_auto_20180905_0347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='division',
            field=models.CharField(choices=[('O', 'Open'), ('X', 'Mixed'), ('W', 'Womens'), ('CO', 'College Open'), ('CW', 'College Womens'), ('YO', 'Youth Open'), ('YX', 'Youth Mixed'), ('YW', 'Youth Womens')], max_length=20),
        ),
    ]