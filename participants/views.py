from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Participant
from .serializers import ParticipantSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404


class ParticipantView(APIView):
    def post(self, request):
        email_address = request.data.get('email_address')
        if Participant.objects.filter(email_address=email_address).exists():
            return Response({'message': 'Registration failed! Email address already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            participant = serializer.save()
            return Response({'message': 'Successfully registered!', 'data': serializer.data, 'participant_id': participant.pk}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        participants = Participant.objects.all()
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data)


    def put(self, request, format=None):
        participant_id = request.data.get('participant_id')
        participant = get_object_or_404(Participant, pk=participant_id)
        serializer = ParticipantSerializer(participant, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Participant profile updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Error occurred during update. Please check your input.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        participant_id = request.data.get('participant_id')
        password = request.data.get('password')

        participants = Participant.objects.filter(participant_id=participant_id)
        if not participants.exists():
            return Response({'error': 'Participant not found'}, status=status.HTTP_404_NOT_FOUND)

        participant = participants.filter(password=password).first()
        if not participant:
            return Response({'error': 'Incorrect password, unable to delete the account'}, status=status.HTTP_400_BAD_REQUEST)

        participant.delete()
        return Response({'message': 'Participant deleted successfully'}, status=status.HTTP_204_NO_CONTENT)




