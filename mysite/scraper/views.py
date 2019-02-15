from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from .forms import ScraperQueryForm
from django.views import View
from django.http import JsonResponse
from .scraper import Scraper
from .models import *
from teams.models import Team
from django.contrib import messages
# Create your views here.
class ScraperView(View):
	template_name = 'scraper/scraper.html'
	success_url = '/teams/scraper/results/'

	def render(self, request, context):
		if(context.get('matched') or context.get('unmatched')):
			num_results=context.get('num_results')

			return render(request, 'teams/scraper_results.html', context)
		return render(request, 'scraper/scraper.html', {'form': self.form})

	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('/401/')
		self.form=ScraperQueryForm()
		context = {}
		return self.render(request, context)

	def post(self, request):
		self.form = ScraperQueryForm(request.POST)
		if self.form.is_valid():
			query = self.form.save(request.user)
			scraper = Scraper(query)
			results = scraper.scrape()
			

			#results = self.form.scrape_data()
			return redirect('/scraper/results/')
		context = {}
		return self.render(request, context)


class ScraperQueryResultsView(View):
	def render(self, request, context):
		return render(request, 'scraper/results.html', context)

	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('/401/')
		queries = request.user.scraper_queries.all()
		context = {
			"queries": queries,
		}
		return self.render(request, context)

class ResultDetailView(View):
	def render(self, request, context):
		return render(request, 'scraper/result_detail.html', context)

	def get_object(self):
		return get_object_or_404(ScraperQuery, pk=self.kwargs.get('pk'))

	def get(self, request, pk):
		self.obj = self.get_object()
		return self.render(request, {"teams": self.obj.teams.all(), "query": self.obj})

def ajax_save_team(request):
	query = get_object_or_404(ScraperQuery, id=request.GET.get('qid', None))
	poolPageTeamInfo = get_object_or_404(PoolPageTeamInfo, id=request.GET.get('tid', None))
	scraper = Scraper(query)
	results = scraper.scrapeTeamEventPage(poolPageTeamInfo.eventTeamURL)
	results.saveTeam()

	#print(results)
	#team = Team(name=poolPageTeamInfo.name, nickname=results["Nickname"], city=results['City'], division=results['Division'], twitterLink=results['Twitter'])
	#team.save()


	messages.success(request, "Successfully saved team")
	return JsonResponse({'saved': True})


def ajax_save_all(request):
	query = get_object_or_404(ScraperQuery, id=request.GET.get('id', None))
	scraper=Scraper(query)
	teams = query.teams.all()
	for t in teams:
		if not (t.thisTeamInDb()):
			results = scraper.scrapeTeamEventPage(t.eventTeamURL)
			results.saveTeam()
	messages.success(request, "Successfully saved teams")
	return JsonResponse({'saved': True})

def ajax_save_eventteam(request):
	t = get_object_or_404(TeamPageData, id=request.GET.get('tid', None))
	t.saveTeam()
	messages.success(request, "Successfully saved team")
	return JsonResponse({'saved': True})

#{'City': 'Washington', 'Competition Level': 'Club', 'Gender Division': 'Men', 'Twitter': 'https://twitter.com/truckstopulti'}
