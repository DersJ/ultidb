from django.contrib import admin
from scraper.models import *


# Register your models here.

class ScraperQueryAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)

class PoolPageTeamInfoAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)

class TeamPageDataAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)

admin.site.register(ScraperQuery, ScraperQueryAdmin)
admin.site.register(PoolPageTeamInfo)
admin.site.register(TeamPageData)