from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django_tables2 import RequestConfig
from teams.models import *
from teams.tables import TeamTable
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.views import View
from teams.forms import ScraperInputForm, ScraperResultsForm, TeamForm
from django.core.exceptions import ValidationError
from django.db.models import Q

import ast


def teamlist(request, *args, **kwargs):
	if('search' in request.GET):
		search_term = request.GET['search']
		print(search_term)
		queryset = Team.objects.filter(Q(name__icontains=search_term)|Q(city__icontains=search_term)|Q(nickname__icontains=search_term))
		table=TeamTable(queryset)
		title = "Search Results"
	else:
		table = TeamTable(Team.objects.all())
		title = "Teams List"
	table.exclude = ('id', 'twitterHandle', 'twitterLink', 'bio', 'nickname')
	RequestConfig(request, paginate={'per_page': 15}).configure(table)
	
	return render(request, 'teams/teamslist.html', {'table': table, 'title': title})

def teamEdit(request, pk=None):
	if not request.user.is_authenticated:
		return redirect('/401/')
	instance = get_object_or_404(Team, pk=pk)
	print(instance)
	if (request.method == 'POST'):
		form = TeamForm(request.POST, instance=instance)
		if(form.is_valid):
			instance = form.save(commit=False)
			instance.save()
			messages.success(request, "Successfully updated team")
			return HttpResponseRedirect(instance.get_absolute_url())
		else:
			messages.error(request, "Error")
	else:
		form = TeamForm(instance=instance)

	context = {
		"team": instance,
		"form": form,
	}
	return render(request, "teams/team_form.html", context)

class TeamDetailView(DetailView):
	queryset = Team.objects.all()

def rosterDetailView(request, id):
	instance = get_object_or_404(Roster, id=id)
	queryset = RosterMembership.objects.filter(roster=instance)

	context = {
		"roster": instance,
		"rm_list": queryset,
		"title": "Roster Detail"
	}
	return render(request, 'teams/roster_detail.html', context)


class ScraperView(View):
	template_name = 'teams/scraper.html'
	success_url = '/teams/scraper/results/'

	def render(self, request, context):
		if(context.get('matched') or context.get('unmatched')):
			num_results=context.get('num_results')

			return render(request, 'teams/scraper_results.html', context)
		return render(request, 'teams/scraper.html', {'form': self.form})

	def post(self, request):
		if request.POST.get('url'):
			self.form = ScraperInputForm(request.POST)
			if self.form.is_valid():
				results = self.form.scrape_data()
				unmatched = results[0]
				matched = results[1]
				num_results = results[2]
				for i in range(len(unmatched)):
					unmatched[i][1].append('<input type="checkbox" class="form-check-input" name="save{0}" id="id_save{0}" checked>'.format(i))
				
				self.form=ScraperResultsForm(num_results=num_results)
				context = {
					"unmatched": unmatched,
					"matched": matched,
					"num_results": num_results,
					'form': self.form
					}

				#return render(request, 'teams/scraper_results.html', context)
				return self.render(request, context)
		elif request.POST.get('Save'):
			unmatched = ast.literal_eval(request.POST.get('unmatched'))
			num_results = len(unmatched)
			self.form = ScraperResultsForm(data=request.POST, num_results=num_results)
			if self.form.is_valid():
				for i in range(num_results):
					if(request.POST.get('save{}'.format(i))):
						info = unmatched[i]
						team = Team(name=info[0], city=info[1][0], division=ScraperView.parseDivison(info[1][1], info[1][2]), twitterLink=info[1][3])
						team.save()
				return HttpResponseRedirect('/teams/scraper/success/')
		context = {"form": self.form}
		return self.render(request, context)

	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('/401/')
		self.form=ScraperInputForm(initial={"url": "https://play.usaultimate.org/events/TCT-Pro-Championships-2018/schedule/Men/Club-Men/"})
		context = {}
		return self.render(request, context)

	def parseDivison(gender, level):
		if("women" in gender.lower() or "girl" in gender.lower()):
			if("club" in level.lower()):
				return "Womens"
			elif("college" in level.lower()):
				return "College Womens"
			elif("youth" in level.lower()):
				return "Youth Womens"
		elif("x" in gender.lower()):
			if("club" in level.lower()):
				return "Mixed"
			elif("college" in level.lower()):
				return "College Mixed"
			elif("youth" in level.lower()):
				return "Youth Mixed"
		elif("men" in gender.lower() or "open" in gender.lower() or "boy" in gender.lower()):
			if("club" in level.lower()):
				return "Open"
			elif("college" in level.lower()):
				return "College Open"
			elif("youth" in level.lower()):
				return "Youth Open"
		
		
		raise ValidationError(_('Division not parsed'), code='invalid_div')

	
class ScraperResults(View):
	def get(self, request):
		context = {}
		return render(request, 'teams/scraper_results.html', context)

