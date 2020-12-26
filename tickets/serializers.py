from tickets.models import Ticket
from rest_framework import serializers
from django.contrib.auth.models import User
from projects.serializers import UserSerializer

class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer()
        model = Ticket
        fields = '__all__'
