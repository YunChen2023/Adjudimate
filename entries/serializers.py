from rest_framework import serializers
from .models import Entry
from participants.models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
    participant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Entry
        fields = ('entry_id', 'entry_name', 'entry_photo', 'entry_audio', 'submit_date', 'update_date', 'run_order', 'entry_status', 'entry_description', 'models_name', 'participant_id', 'category')  # Add or remove fields as needed

    def create(self, validated_data):
        participant_id = validated_data.pop('participant_id')
        participant = Participant.objects.get(pk=participant_id)
        return Entry.objects.create(participant=participant, **validated_data)

    def update(self, instance, validated_data):
        participant_id = validated_data.pop('participant_id', None)
        if participant_id is not None:
            instance.participant = Participant.objects.get(pk=participant_id)
        return super().update(instance, validated_data)
