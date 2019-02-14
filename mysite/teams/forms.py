from django import forms
from .scraper import Scraper
from .models import Team
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class ScraperInputForm(forms.Form):
	url = forms.CharField()
	type_choices = forms.ChoiceField(choices=[("A","A"), ("B","B")])
	def clean_url(self):
		val = URLValidator()
		url = self.cleaned_data['url']
		val(url)
		if(url.split('//')[1][:20] != 'play.usaultimate.org'):
			raise ValidationError(_('Url not usaultimate.org'), code='not_usau')
		return url

	def scrape_data(self):
		
		url = self.cleaned_data['url']
		
		return Scraper.scrapePoolsPage(url)

class ScraperResultsForm(forms.Form):
	
	def __init__(self, num_results, *args, **kwargs):
		super(ScraperResultsForm, self).__init__(*args, **kwargs)
		#self.results = results
		for i in range(num_results):
			self.fields['save'+str(i)] = forms.BooleanField(required=False)

class TeamForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = [
			"name",
			"nickname",
			"city",
			"bio",
			"twitterLink",

		]