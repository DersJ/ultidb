from django.contrib import admin
from teams.models import *
# Register your models here.
admin.site.register(Team)
admin.site.register(Person)
admin.site.register(Player)
admin.site.register(RosterCoachMembership)
admin.site.register(Roster)
admin.site.register(RosterMembership)