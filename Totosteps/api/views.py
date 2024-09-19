from django.shortcuts import render

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
