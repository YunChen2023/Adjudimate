from django.db import connection
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from django.shortcuts import get_object_or_404

class LoginView(APIView):
    def get(self, request):
        email_address = request.query_params.get('email_address')
        password = request.query_params.get('password')
        
        with connection.cursor() as cursor:
            # Check users_user table
            cursor.execute("SELECT user_id, user_role FROM users_user WHERE email_address = %s AND password = %s", [email_address, password])
            row = cursor.fetchone()

            if row is not None:
                return Response({'message': 'Login successfully!', 'user_id': row[0], 'user_role': row[1]}, status=status.HTTP_200_OK)

            # Check participants_participant table
            cursor.execute("SELECT participant_id, participant_role FROM participants_participant WHERE email_address = %s AND password = %s", [email_address, password])
            row = cursor.fetchone()

            if row is not None:
                return Response({'message': 'Login successfully!', 'participant_id': row[0], 'participant_role': row[1]}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid Email or Password!'}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request):
        users = User.objects.values()
        return Response(list(users))


    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            if user.user_role == 'Judge':
                message = 'Successfully added a new judge!'
            elif user.user_role == 'Adjudicator':
                message = 'Successfully added a new adjudicator!'
            elif user.user_role == 'Admin':
                message = 'Admin user created successfully!'
            return Response({'message': message, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User profile updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'message': 'Error occurred during update. Please check your input.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Get user_id and password from the request's Body
        user_id = request.data.get('user_id')
        password = request.data.get('password')

        # Get the user
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=400)

        # Verify the password
        if password == user.password:
            # If the verification is successful, delete the user
            user.delete()
            return Response({"message": "User has been successfully deleted"})
        else:
            # If the verification fails, return an error message
            return Response({"message": "Incorrect password"}, status=400)



