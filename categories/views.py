from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, Category
from .serializers import CategorySerializer
from rest_framework import status

class CategoryAPI(APIView):
    def post(self, request):
        event_pk = request.data.get('event_id')
        event = get_object_or_404(Event, pk=event_pk)
        data = request.data
        data['event'] = event_pk
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            category = serializer.save()
            return Response({'message': 'Category created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Category creation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        event_id = request.data.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        categories = event.categories.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        category_id = request.data.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        data = request.data
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Category update failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        category_id = request.data.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        category.delete()
        return Response({'message': 'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
