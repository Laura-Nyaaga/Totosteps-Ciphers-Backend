from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from dateutil.relativedelta import relativedelta
from child.models import Child
from .serializers import  ChildSerializer
from django.utils import timezone

<<<<<<< HEAD



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
=======
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from autism_results.models import Autism_Results
from autism_image.models import Autism_Image

from .serializers import AutismImageSerializer
from .serializers import AutismResultsSerializer


class AutismImageListView(APIView):

    def get(self, request):
        images = Autism_Image.objects.all()
        serializer = AutismImageSerializer(images, many=True)
        return Response(serializer.data)
     
    def post(self, request):
        serializer = AutismImageSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save()  
            return Response(AutismImageSerializer(photo).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AutismImageDetailListView(APIView):
     
    def get(self, request, image_id):
        try:
            image = Autism_Image.objects.get(image_id=image_id)
            serializer = AutismImageSerializer(image)
            return Response(serializer.data)
        except Autism_Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
     

    
    def delete(self, request, image_id):
        try:
            image = Autism_Image.objects.get(image_id=image_id)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Autism_Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

        

class AutismResultListView(APIView):
    """
    Handles retrieving a list of all autism results.
    """
    def get(self, request):
        autism_results = Autism_Results.objects.all()  # Retrieve all autism results
        serializer = AutismResultsSerializer(autism_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AutismResultsSerializer(data=request.data)
        if serializer.is_valid():
            autism_result = serializer.save()  # Save the uploaded autism result
            return Response(AutismResultsSerializer(autism_result).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class AutismResultDetailListView(APIView):
    """
    Handles retrieving and deleting an autism result by its ID.
    """
    def get(self, request, image_id):
        try:
            autism_result = Autism_Results.objects.get(image_id=image_id)
            return Response(AutismResultsSerializer(autism_result).data, status=status.HTTP_200_OK)
        except Autism_Results.DoesNotExist:
            return Response({"error": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
    

    def delete(self, request, image_id):
        try:
            autism_result = Autism_Results.objects.get(image_id=image_id)
            autism_result.delete()  # Delete the autism result
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Autism_Results.DoesNotExist:
            return Response({"error": "Photo not found."}, status=status.HTTP_404_NOT_FOUND)
>>>>>>> 28d6f20 (add autism results and the image)
