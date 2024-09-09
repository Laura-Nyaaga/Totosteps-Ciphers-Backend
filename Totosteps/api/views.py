from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .serializers import ChildSerializer


class ParentDetailAPIView(APIView):
    def get(self, request, parent_id):
        parent = get_object_or_404(User, parent_id=parent_id)
        serializer = ParentSerializer(parent)
        return Response(serializer.data)

class SignInAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data   

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key},   
 status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class SignUpAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,   
 status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class ParentUpdateAPIView(APIView):
    def put(self, request, parent_id):
        parent = get_object_or_404(User, parent_id=parent_id)
        serializer = UserSerializer(parent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, 
 status=status.HTTP_400_BAD_REQUEST) 

class ParentChildrenAPIView(APIView):
    def get(self, request, parent_id):
        parent = get_object_or_404(User, parent_id=parent_id)
        children = parent.children.all()
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)