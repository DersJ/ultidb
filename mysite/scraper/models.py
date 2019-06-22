from django.db import models
from mysite import settings
from teams.models import Team

# Create your models here.
class ScraperQuery(models.Model):
	class Meta:
		ordering = ['-created']
	TYPE_CHOICES = (
		('PP', "Pools Page"),
		('TP', "Team Page"),
		('ET', "Event Team Page"))
	DIVISION_CHOICES = (
    ('O', 'Open'),
    ('X', 'Mixed'),
    ('W', 'Womens'),
    ('CO', 'College Open'),
    ('CW', 'College Womens'),
    ('YO', 'Youth Open'),
    ('YX', 'Youth Mixed'),
    ('YW', 'Youth Womens'),)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scraper_queries')
	tournament = models.CharField(max_length=100, blank=True)
	division = models.CharField(max_length=2, choices=DIVISION_CHOICES, verbose_name="Division", help_text="Select the division for this page")
	pageType = models.CharField(max_length=2, choices=TYPE_CHOICES, verbose_name="Page Type", help_text="Select your page type")
	url=models.URLField(verbose_name="URL", help_text="Link to a USA Ultimate page")
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		formatedDate = self.created.strftime("%m/%d/%Y, %I:%M:%S %p")
		return '%s query at %s' % (self.get_pageType_display(), formatedDate)

class PoolPageTeamInfo(models.Model):
	match_url = models.CharField(default="", blank=True, max_length=200)
	name = models.CharField(max_length=200)
	seed = models.IntegerField()
	poolSeed = models.IntegerField(default=0)
	eventTeamURL = models.URLField()
	created = models.DateTimeField(auto_now_add=True)
	query = models.ForeignKey(ScraperQuery, on_delete=models.CASCADE, related_name='teams')

	def __str__(self):
		return '%s seeded %s' % (self.name, self.seed)

	def thisTeamInDb(self):
		print(self.name)
		if Team.objects.filter(name__contains=self.name).filter(division=self.query.division):
			match = Team.objects.filter(name__contains=self.name)[0]
			match_url = "/teams/%d/" % match.id
			return match_url
		else:
			return ""


class TeamPageData(models.Model):
	name = models.CharField(max_length=200)
	nickname = models.CharField(max_length=200, default="")
	city = models.CharField(max_length=50)
	division = models.CharField(max_length=20)
	twitterLink = models.URLField(max_length=200, default='http://www.twitter.com')
	created = models.DateTimeField(auto_now_add=True)
	query = models.ForeignKey(ScraperQuery, on_delete=models.CASCADE, related_name='team')


	def thisTeamInDb(self):
		if Team.objects.filter(name__contains=self.name):
			match = Team.objects.filter(name__contains=self.name)[0]
			match_url = "/teams/%d/" % match.id
			return match_url
		else:
			return ""

	def saveTeam(self):
		if self.thisTeamInDb():
			print("already matched!")
		else:
			print("saving...")
			t = Team(name=self.name, nickname=self.nickname, city=self.city, division=self.division, twitterLink=self.twitterLink)
			t.save()
			print(t)
	def __str__(self):
		return '%s' % (self.name)