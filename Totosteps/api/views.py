from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from child.models import Child
from .serializers import ChildSerializer
from autism_results.models import Autism_Results
from autism_image.models import Autism_Image
from .serializers import AutismImageSerializer, AutismResultsSerializer

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
        image = get_object_or_404(Autism_Image, image_id=image_id)
        serializer = AutismImageSerializer(image)
        return Response(serializer.data)
     
    def delete(self, request, image_id):
        image = get_object_or_404(Autism_Image, image_id=image_id)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AutismResultListView(APIView):
    def get(self, request):
        autism_results = Autism_Results.objects.all()
        serializer = AutismResultsSerializer(autism_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AutismResultsSerializer(data=request.data)
        if serializer.is_valid():
            autism_result = serializer.save()
            return Response(AutismResultsSerializer(autism_result).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AutismResultDetailListView(APIView):
    def get(self, request, result_id):  # Changed to result_id for clarity
        autism_result = get_object_or_404(Autism_Results, id=result_id)
        return Response(AutismResultsSerializer(autism_result).data, status=status.HTTP_200_OK)

    def delete(self, request, result_id):  # Changed to result_id for clarity
        autism_result = get_object_or_404(Autism_Results, id=result_id)
        autism_result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChildListView(APIView):
    def get(self, request):
        children = Child.objects.filter(is_active=True)  # Filter for active children
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChildDetailView(APIView):
    def get_object(self, child_id):
        return get_object_or_404(Child, id=child_id, is_active=True)

    def put(self, request, child_id):
        child = self.get_object(child_id)
        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, child_id):
        child = self.get_object(child_id)
        child.is_active = False
        child.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
