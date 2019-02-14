from django.db import models
from enum import Enum
from django.urls import reverse
#from ultimodels import *
# Create your models here.

class Division(Enum):
	OPEN = "Open"
	MIXED = "Mixed"
	WOMENS = "Womens"
	COLLEGEOPEN = "College Open"
	COLLEGEWOMENS = "College Womens"
	YOUTHOPEN = "Youth Open"
	YOUTHMIXED = "Youth Mixed"
	YOUTHWOMENS = "Youth Womens"



class Team(models.Model):
	DIVISION_CHOICES = (
    ('O', 'Open'),
    ('X', 'Mixed'),
    ('W', 'Womens'),
    ('CO', 'College Open'),
    ('CW', 'College Womens'),
    ('YO', 'Youth Open'),
    ('YX', 'Youth Mixed'),
    ('YW', 'Youth Womens'),)

	name = models.CharField(max_length=50)
	nickname = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=50)
	division = models.CharField(max_length=20, choices=DIVISION_CHOICES, blank=False)
	bio = models.TextField(default="No bio yet.")
	#logo = models.FileField(null=True, blank=True)
	rosters = models.ManyToManyField('Roster', blank=True)
	twitterHandle = models.CharField(max_length=50, null=True)
	twitterLink = models.URLField(max_length=200, default='http://www.twitter.com')
	updated = models.DateTimeField(auto_now=True)
	
	def get_absolute_url(self):
		return reverse("team_detail", kwargs={"pk": self.pk})


	def __str__(self):
		return self.name

	#def printStats(self):
	#	print(self.name+ " is from " + self.city + " and plays in the " + self.division.value.lower() + " division.")

#Players relate to teams and games through Rosters in a many to many relationship


class Person(models.Model):
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name+" "+self.last_name

class Player(Person):
	career_goals=models.IntegerField(default=0)
	career_assists=models.IntegerField(default=0)
	career_blocks=models.IntegerField(default=0)
	#current_team = models.ForeignKey(Team, on_delete=models.CASCADE) to implement later
	

class Roster(models.Model):
	year = models.IntegerField(default=2018)
	associated_team = models.ForeignKey(Team, on_delete=models.CASCADE)
	#games = models.ManyToManyField(Game, blank = True, related_name='games')
	players = models.ManyToManyField(Player, through='RosterMembership', related_name='playsOn')
	updated = models.DateTimeField(auto_now=True)
	coaches = models.ManyToManyField(Person, through='RosterCoachMembership', related_name='coaches')

	def __str__(self):
		return self.associated_team.name + " " + str(self.year)


class Game(models.Model):
	date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
	rosters = models.ManyToManyField(Roster, through='GameMembership')

#using extra fields in the many-to-many relationship between roster and player. Roster has members through RosterMembership
#https://docs.djangoproject.com/en/dev/topics/db/models/#extra-fields-on-many-to-many-relationships
class RosterMembership(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
	number = models.IntegerField(default=0)

	def __str__(self):
		return str(self.player)+" plays on "+str(self.roster)

class RosterCoachMembership(models.Model):
	ROLE_CHOICES = (
    ('H', 'Head'),
    ('A', 'Assistant'),)

	coach = models.ForeignKey(Person, on_delete=models.CASCADE)
	roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES)
	

	def __str__(self):
		return str(self.coach)+" coaches "+str(self.roster)

class GameMembership(models.Model):
	roster = models.ForeignKey(Roster, on_delete=models.CASCADE)
	game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Tournament(models.Model):
	games = models.ManyToManyField(Game)
	teams = models.ManyToManyField(Team)


