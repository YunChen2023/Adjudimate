from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Criterion
from .serializers import CriterionSerializer
from rest_framework import status

class CriterionAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = CriterionSerializer(data=data)
        if serializer.is_valid():
            criterion = serializer.save()
            return Response({'message': 'Criterion created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Criterion creation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        criterion_id = request.data.get('criterion_id')
        criterion = get_object_or_404(Criterion, pk=criterion_id)
        data = request.data
        serializer = CriterionSerializer(criterion, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Criterion updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Criterion update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        criterion_id = request.data.get('criterion_id')
        criterion = get_object_or_404(Criterion, pk=criterion_id)
        criterion.delete()
        return Response({'message': 'Criterion deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
