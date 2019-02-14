from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.urls import path, re_path
from teams import views
from teams.models import Team

urlpatterns = [
    url(r'^$', views.teamlist, name='teamlist'),
    #url(r'^scraper/$', views.ScraperView.as_view()),
    #url(r'^scraper/success/$', TemplateView.as_view(template_name='teams/scraper_success.html')),
    url(r'^(?P<pk>\w+)/$', views.TeamDetailView.as_view(), name='team_detail'),
    url(r'^rosters/(?P<id>\d+)/$', views.rosterDetailView, name='roster_detail'),
    re_path(r'^(?P<pk>\w+)/edit/$', views.teamEdit, name='edit'),
    

]
