from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notice
from .serializers import NoticeSerializer
from events.models import Event

class NoticeAPI(APIView):
    def post(self, request):
        event_id = request.data.get('event_id')
        notice_tab = request.data.get('notice_tab')
        notice = request.data.get('notice')

        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        notice = Notice.objects.create(
            event=event,
            notice_tab=notice_tab,
            notice=notice
        )

        serializer = NoticeSerializer(notice)
        return Response({
            'message': f'Successfully created notice for {notice_tab}',
            'notice': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        event_id = request.data.get('event_id')
        
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        notices = Notice.objects.filter(event=event)
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)


    def put(self, request):
        event_id = request.data.get('event_id')
        notice_id = request.data.get('notice_id')

        try:
            event = Event.objects.get(event_id=event_id)
            notice = Notice.objects.get(id=notice_id)
        except (Event.DoesNotExist, Notice.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            if hasattr(notice, key):
                setattr(notice, key, value)

        notice.save()

        serializer = NoticeSerializer(notice)
        return Response({
            'message': f'Successfully updated notice',
            'notice': serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        notice_id = request.data.get('notice_id')

        try:
            notice = Notice.objects.get(id=notice_id)
        except (Event.DoesNotExist, Notice.DoesNotExist):
            return Response({'message': f'Notice not exist'}, 
                            status=status.HTTP_404_NOT_FOUND)

        notice.delete()
        return Response({
            'message': f'Successfully deleted notice'
        }, status=status.HTTP_204_NO_CONTENT)
