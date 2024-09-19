from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta
from child.models import Child
from .serializers import  ChildSerializer
from django.utils import timezone




class ChildListView(APIView):
    def get(self, request):
        children = Child.objects.all()
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)

    # Create a new child record
    def post(self, request):
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChildDetailView(APIView):
    # Retrieve a child by ID
    def get_object(self, child_id):
        return get_object_or_404(Child, id=child_id, is_active=True)

    # Update the details of the child
    def put(self, request, child_id):
        child = self.get_object(child_id)
        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Soft delete child 
    def delete(self, request, child_id):
        child = self.get_object(child_id)
        child.is_active = False
        child.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
