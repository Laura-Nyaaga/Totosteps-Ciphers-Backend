import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)
class UserListView(APIView):
    """
    This view returns a list of all users in the system.
    It uses the `UserSerializer` to serialize the user data and logs the retrieval.
    """
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info("Retrieved user list.")
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    """
    This view handles retrieving, updating, and deleting a specific user by their ID.
    It supports GET, PUT, PATCH, and DELETE operations.
    - GET: Retrieves user details.
    - PUT: Updates all user data.
    - PATCH: Partially updates user data.
    - DELETE: Soft deletes the user by setting their `is_active` field to False.
    """
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            logger.info(f"Retrieved details for user {user.username}.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User {user.username} updated successfully.")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.warning(f"Failed to update user {user.username}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User {user.username} partially updated successfully.")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.warning(f"Failed to partially update user {user.username}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.is_active = False
            user.save()
            logger.info(f"User {user.username} soft-deleted successfully.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    """
    This view handles the user registration process.
    It validates the provided registration data, creates a new user, and logs the event.
    If registration fails, it logs the error and returns validation errors.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            logger.info(f"User {user.username} registered successfully.")
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)