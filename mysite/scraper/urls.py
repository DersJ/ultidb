from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.urls import path, re_path
from scraper import views


urlpatterns = [
	url(r'^$', views.ScraperView.as_view(), name='scraper'),
	path('results/', views.ScraperQueryResultsView.as_view(), name='results'),
	path('results/<int:pk>/', views.ResultDetailView.as_view(), name='result-detail'),
	path('ajax_save_team/', views.ajax_save_team, name='ajax-save-team'),
	path('ajax_save_all/', views.ajax_save_all, name='ajax-save-all'),
	path('ajax_save_eventteam/', views.ajax_save_eventteam, name='ajax-save-eventteam'),

]