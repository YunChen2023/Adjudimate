from rest_framework import generics
from .models import Entry
from events.models import Event
from categories.models import Category
from participants.models import Participant
from .serializers import EntrySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework.parsers import MultiPartParser, FormParser
  

class RejectEntryView(APIView):
    def put(self, request, format=None):
        entry_id = request.data.get('entry_id')
        
        if not entry_id:
            return Response({"message": "Entry ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            entry = Entry.objects.get(pk=entry_id)
        except Entry.DoesNotExist:
            return Response({"message": "Entry not found."}, status=status.HTTP_404_NOT_FOUND)

        if entry.entry_status != 'Pending Review':
            return Response({"message": "Entry is not pending review."}, status=status.HTTP_400_BAD_REQUEST)

        entry.entry_status = 'Rejected'
        entry.save()

        return Response({"message": "Entry has been rejected successfully."}, status=status.HTTP_200_OK)



class AcceptEntryView(APIView):
    def put(self, request, format=None):
        entry_id = request.data.get('entry_id')
                
        if not entry_id:
            return Response({'error': 'Entry ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        entry = get_object_or_404(Entry, pk=entry_id)

        if entry.run_order is not None:
            return Response({'error': 'Run order has already been assigned'}, status=status.HTTP_400_BAD_REQUEST)
        
        entry.entry_status = 'Approved'
        
        category_id = entry.category.category_id
        max_run_order = Entry.objects.filter(category_id=category_id).aggregate(Max('run_order'))['run_order__max'] or 0
        entry.run_order = max_run_order + 1
        entry.save()
        
        return Response({'message': 'The entry_id has been successfully accepted', 'run_order': entry.run_order}, status=status.HTTP_200_OK)



class MaxRunOrderView(APIView):
    def get(self, request, format=None):
        category_id = request.data.get('category_id')
        if not category_id:
            return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        max_run_order = Entry.objects.filter(category_id=category_id).aggregate(Max('run_order'))['run_order__max']
        return Response({'max_run_order': max_run_order})
    


class AddModelsView(APIView):
    def post(self, request):
        entry_id = request.data.get('entry_id')
        models_name = request.data.get('models_name')

        try:
            entry = Entry.objects.get(entry_id=entry_id)
        except Entry.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        entry.models_name = models_name
        entry.save()

        return Response({'message': f'Successfully added models_name to entry {entry_id}'}, status=status.HTTP_200_OK)


class EntryView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = EntrySerializer
 
    def post(self, request, format=None):
        category_id = request.data.get('category_id')
        participant_id = request.data.get('participant_id')

        try:
            category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = Participant.objects.get(participant_id=participant_id)
        except Participant.DoesNotExist:
            return Response({'message': 'Participant not found!'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['category'] = category.pk
        request.data['participant'] = participant.pk

        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            entry = serializer.save()

            if 'entry_photo' in request.data:
                entry.entry_photo = request.data['entry_photo']
                entry.save()

            return Response({'message': 'Entry created and photo uploaded successfully!', 'entry': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        entry_id = request.data.get('entry_id')
        if entry_id is not None:
            try:
                entry = Entry.objects.get(entry_id=entry_id)
                entry.delete()
                return Response({'message': 'Entry deleted successfully!'}, status=status.HTTP_200_OK)
            except Entry.DoesNotExist:
                return Response({'message': 'Entry not found!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'No entry_id provided!'}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        entry_id = request.data.get('entry_id')
        entry_name = request.data.get('entry_name')
        category_name = request.data.get('category_name')
        entry_description = request.data.get('entry_description')

        if entry_id is not None:
            try:
                entry = Entry.objects.get(entry_id=entry_id)
                if entry_name is not None:
                    entry.entry_name = entry_name
                if category_name is not None:
                    category = Category.objects.get(category_name=category_name)
                    entry.category = category
                if entry_description is not None:
                    entry.entry_description = entry_description
                entry.save()
                return Response({
                'message': 'Entry updated successfully!',
                'entry_id': entry.entry_id,
                'entry_name': entry.entry_name,
                'category_name': entry.category.category_name,
                'entry_description': entry.entry_description
            }, status=status.HTTP_200_OK)
            except Entry.DoesNotExist:
                return Response({'message': 'Entry not found!'}, status=status.HTTP_404_NOT_FOUND)
            except Category.DoesNotExist:
                return Response({'message': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'No entry_id provided!'}, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        entry_id = self.request.data.get('entry_id')
        if not entry_id:
            return Entry.objects.all()  # Return all entries
        return Entry.objects.filter(entry_id=entry_id)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"message": "No entries found."}, status=status.HTTP_404_NOT_FOUND)
        
        if queryset.count() == 1:
            instance = queryset.first()
            response = {
                'entry_name': instance.entry_name,
                'entry_description': instance.entry_description,
                'entry_photo': request.build_absolute_uri(instance.entry_photo.url) if instance.entry_photo else None,
                'participant_first_name': instance.participant.first_name,
                'participant_last_name': instance.participant.last_name,
                'submit_date': instance.submit_date,
                'update_date': instance.update_date
            }
            return Response(response)
        
        response = []
        for instance in queryset:
            entry_data = {
                'entry_name': instance.entry_name,
                'entry_description': instance.entry_description,
                'entry_photo': request.build_absolute_uri(instance.entry_photo.url) if instance.entry_photo else None,
                'participant_first_name': instance.participant.first_name,
                'participant_last_name': instance.participant.last_name,
                'submit_date': instance.submit_date,
                'update_date': instance.update_date
            }
            response.append(entry_data)
        return Response(response)
