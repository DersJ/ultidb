from django import forms
from .models import ScraperQuery
from .scraper import Scraper
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class ScraperQueryForm(forms.ModelForm):
	class Meta:
		model = ScraperQuery
		fields = [
			"url",
			"pageType",
		]
		exclude = ('user',)

	def save(self, user, commit=True):
		self.instance.user = user
		return super().save(commit=commit)

	def clean_url(self):
		val = URLValidator()
		url = self.cleaned_data['url']
		val(url)
		if(url.split('//')[1][:20] != 'play.usaultimate.org'):
			raise ValidationError(_('Url not usaultimate.org'), code='not_usau')
		return url
		
	def scrape_data(self):
		url = self.cleaned_data['url']
		pageType = self.cleaned_data['pageType']
		if(pageType == "PP"):
			return Scraper.scrapePoolsPage(url)
		elif(pageType == "TP"):
			return Scraper.scrapeTeamPage(url)
		elif(pageType == "ET"):
			return Scraper.scrapeEventTeamPage(url)