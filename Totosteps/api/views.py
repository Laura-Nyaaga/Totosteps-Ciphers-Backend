import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


logger = logging.getLogger(__name__)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        """
        Retrieve a list of all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info("Retrieved user list.")
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        """
        Handle user registration.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User registered successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('User registration failed: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        """
        Handle user login.
        """
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            logger.info('User logged in successfully.')
            return Response({
                'success': 'Successfully logged in.',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        
        logger.error('Invalid credentials provided for login.')
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle user logout.
        """
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  
            logger.info('User logged out successfully.')
            return Response({'success': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error('Logout error: %s', str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
