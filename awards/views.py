from .models import Award
from .models import Event
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AwardView(APIView):
   
    def get(self, request, format=None):
        event_id = request.data.get('event_id', None)
        if event_id is not None:
            awards = Award.objects.filter(event_id=event_id)
            data = [{"award_id": award.award_id, "award_type": award.award_type, "award_description": award.award_description} for award in awards]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "event_id not provided"}, status=status.HTTP_400_BAD_REQUEST)
 

    def post(self, request, format=None):
        event_id = request.data.get('event_id', None)
        award_type = request.data.get('award_type', None)
        award_description = request.data.get('award_description', None)

        if event_id is not None and award_type is not None:
            event = Event.objects.get(event_id=event_id)
            award = Award(award_type=award_type, award_description=award_description, event=event)
            award.save()
            return Response({"success": "Award created successfully", "award_id": award.award_id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "event_id or award_type not provided"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        award_id = request.data.get('award_id', None)
        award_type = request.data.get('award_type', None)
        award_description = request.data.get('award_description', None)

        if award_id is not None:
            try:
                award = Award.objects.get(award_id=award_id)
                update_fields = {}
                if award_type is not None:
                    update_fields['award_type'] = award_type
                if award_description is not None:
                    update_fields['award_description'] = award_description
                Award.objects.filter(award_id=award_id).update(**update_fields)
                award.refresh_from_db()  # Refresh the instance from the database
                return Response({"success": "Award updated successfully", "updated_fields": update_fields}, status=status.HTTP_200_OK)
            except Award.DoesNotExist:
                return Response({"error": "Award with the given award_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "award_id not provided"}, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, format=None):
        award_id = request.data.get('award_id', None)

        if award_id is not None:
            try:
                award = Award.objects.get(award_id=award_id)
                award.delete()
                return Response({"success": "Award deleted successfully"}, status=status.HTTP_200_OK)
            except Award.DoesNotExist:
                return Response({"error": "Award with the given award_id does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "award_id not provided"}, status=status.HTTP_400_BAD_REQUEST)
