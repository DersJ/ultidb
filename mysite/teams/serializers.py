from teams.models import *
from rest_framework import serializers

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'nickname', 'city', 'division', 'bio')

