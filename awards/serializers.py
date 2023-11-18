from rest_framework import serializers
from .models import Award
from events.models import Event
from participants.models import Participant

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class AwardSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)
    class Meta:
        model = Award
        fields = '__all__'
