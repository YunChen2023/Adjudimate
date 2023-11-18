from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event
from .serializers import EventSerializer
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

class EventAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        event_serializer = EventSerializer(data=request.data)
        if event_serializer.is_valid():
            event_serializer.save()
            return Response({'message': 'New event created successfully', 'data': event_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Event updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Event update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        event.delete()
        return Response({'message': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)
        if query is not None:
            try:
                event = Event.objects.get(event_name__iexact=query)
            except Event.DoesNotExist:
                raise NotFound("Event not found.")
            event_data = {
                'event_id': event.pk,
                'event_name': event.event_name,
            }
            return Response({'event': event_data}, status=status.HTTP_200_OK)
        else:
            events = Event.objects.all()
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
