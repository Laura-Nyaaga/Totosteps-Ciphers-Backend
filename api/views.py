
from rest_framework.views import APIView 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Permission
from django.core.files.storage import default_storage
from django.db import transaction
import logging

import cv2
import numpy as np
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from assessment.models import Assessment
from child.models import Child
from autism_image.models import Autism_Image
from autism_results.models import Autism_Results

from milestones.models import Milestone
from resources.models import Resource
from result.models import Result
from result.utils import send_results_email
from .serializers import (AssessmentSerializer,
ChildSerializer,
MilestoneSerializer, 
ResourceSerializer, 
ResultSerializer,
RegisterSerializer)
from .serializers import AutismImageSerializer, AutismResultsSerializer


lower_ipd_threshold = 4.0  # cm
upper_ipd_threshold = 5.0   # cm
high_autism_ipd_threshold = upper_ipd_threshold + 1  # cm
lower_forehead_threshold = 3.5  # cm
upper_forehead_threshold = 4.5   # cm
high_autism_forehead_threshold = upper_forehead_threshold + 1
scale_factor = 30.0 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


User = get_user_model()
logger = logging.getLogger(__name__)

# AUTISM IMAGE

class AutismImageUploadView(APIView):
    def post(self, request):
        # Handle file upload
        file = request.FILES['image']
        file_name = default_storage.save(file.name, file)
        file_path = default_storage.path(file_name)

        # Load the uploaded image using OpenCV
        image = cv2.imread(file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return Response({"error": "No face detected"}, status=status.HTTP_400_BAD_REQUEST)

        for face_coordinates in faces:
            # Calculate measurements
            eye_distance_cm, forehead_length_cm, left_eye, right_eye = self.calculate_measurements(face_coordinates)

            # Assess autism risk
            risk_assessment = self.assess_risk(eye_distance_cm, forehead_length_cm)

            # Save the image and result to the database
            autism_image = Autism_Image.objects.create(image_upload=file_name)  
            autism_result = Autism_Results.objects.create(
                image=autism_image,
                result=risk_assessment
            )

            result_serializer = AutismResultsSerializer(autism_result)

            # Return the result
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)

    def calculate_measurements(self, face_coordinates):
        """Calculate inter-pupillary distance (IPD) and forehead length."""
        x, y, w, h = face_coordinates
        left_eye = (x + int(w * 0.25), y + int(h * 0.4))
        right_eye = (x + int(w * 0.75), y + int(h * 0.4))
        forehead_top = (x + int(w * 0.5), y)
        forehead_bottom = (x + int(w * 0.5), y + int(h * 0.3))
        pixel_distance_ipd = np.linalg.norm(np.array(left_eye) - np.array(right_eye))
        eye_distance_cm = pixel_distance_ipd / scale_factor
        pixel_distance_forehead = np.linalg.norm(np.array(forehead_top) - np.array(forehead_bottom))
        forehead_length_cm = pixel_distance_forehead / scale_factor
        return eye_distance_cm, forehead_length_cm, left_eye, right_eye

    def assess_risk(self, eye_distance_cm, forehead_length_cm):
        """Assess autism risk based on IPD and forehead length."""
        if (eye_distance_cm > high_autism_ipd_threshold) and (forehead_length_cm > high_autism_forehead_threshold):
            return "Highly Autistic"
        elif (lower_ipd_threshold <= eye_distance_cm <= upper_ipd_threshold) and (lower_forehead_threshold <= forehead_length_cm <= upper_forehead_threshold):
            return "Non Autistic"
        else:
            return "Low Autism Risk"
    def get(self, request):
        images = Autism_Image.objects.all()
        serializer = AutismImageSerializer(images, many=True)
        return Response(serializer.data)
     
class AutismImageDetailListView(APIView):
    def get(self, request, image_id):
        image = get_object_or_404(Autism_Image, image_id=image_id)
        serializer = AutismImageSerializer(image)
        return Response(serializer.data)
     
    def delete(self, request, image_id):
        image = get_object_or_404(Autism_Image, image_id=image_id)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# AUTISM RESULT

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
    def get(self, request, result_id): 
        autism_result = get_object_or_404(Autism_Results, id=result_id)
        return Response(AutismResultsSerializer(autism_result).data, status=status.HTTP_200_OK)

    def delete(self, request, result_id):  
        autism_result = get_object_or_404(Autism_Results, id=result_id)
        autism_result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CHILD MODEL
class ChildListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        children = Child.objects.filter(parent=request.user, is_active=True)
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(parent=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChildDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, child_id):
        return get_object_or_404(Child, child_id=child_id, parent=self.request.user, is_active=True)

    def get(self, request, child_id):
        child = self.get_object(child_id)
        serializer = ChildSerializer(child)
        return Response(serializer.data)

    def delete(self, request, child_id):
        child = self.get_object(child_id)
        child.is_active = False
        child.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# MILESTONE MODEL  
class MilestoneListView(APIView):
    def get(self, request):
        milestones = Milestone.objects.all()
        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MilestoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MilestoneDetailView(APIView):
    def get_object(self, milestone_id):
        return get_object_or_404(Milestone, milestone_id=milestone_id)

    def get(self, request, milestone_id):
        milestone = self.get_object(milestone_id)
        serializer = MilestoneSerializer(milestone)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, milestone_id):
        milestone = self.get_object(milestone_id)
        serializer = MilestoneSerializer(milestone, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, milestone_id):
        milestone = self.get_object(milestone_id)
        milestone.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ChildMilestoneListView(APIView):
    def get(self, request, child_id):
        child = get_object_or_404(Child, child_id=child_id)
        child_age_in_months = child.get_age_in_months()
        current_milestone = Milestone.get_current_milestone(child_age_in_months)
        milestones = Milestone.objects.filter(child_id=child).order_by('age')
        milestone_data = []
        for milestone in milestones:
            is_current = (milestone == current_milestone)
            milestone_data.append({
                "id": milestone.milestone_id,
                "age": milestone.age,
                "description": milestone.name,
                "summary": milestone.summary,
                "is_current": is_current
            })
        return Response(milestone_data, status=status.HTTP_200_OK)


 # ASSESSMENT MODEL
class AssessmentListView(APIView):
    def post(self, request):
        serializer = AssessmentSerializer(data=request.data)

        if serializer.is_valid():
            milestone_id = request.data.get('milestone')
            if not Milestone.objects.filter(milestone_id=milestone_id).exists():
                return Response(
                    {"error": "Milestone not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer.save()
            return Response(
                {
                    "message": "Assessment question created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": "Invalid data",
                "details": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get(self, request):
        questions = Assessment.objects.all()
        serializer = AssessmentSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# GET, UPDATE AND DELETE A SPECIFIC QUESTION
class AssessmentDetailView(APIView):
    def get(self, request, question_id):
        question = get_object_or_404(Assessment, question_id=question_id)
        serializer = AssessmentSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, question_id):
        question = get_object_or_404(Assessment, question_id=question_id)
        serializer = AssessmentSerializer(question, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = get_object_or_404(Assessment, question_id=question_id)
        question.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# GET QUESTIONS UNDER A SPECIFIC MILESTONE
class MilestoneQuestionsListView(APIView):
    def get(self, request, milestone_id):
        milestone = get_object_or_404(Milestone, milestone_id=milestone_id)
        questions = Assessment.objects.filter(milestone=milestone)
        serializer = AssessmentSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# LIST QUESTIONS BY CATEGORY
class CategoryQuestionsListView(APIView):
    def get(self, request, category):
        questions = Assessment.objects.filter(category=category)
        if not questions:
            return Response({"error": "No questions found for this category."}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssessmentSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   

# RESULT MODEL

class ResultListView(APIView):

    def get(self, request): 
        results = Result.objects.all() 
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ResultSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            result = serializer.save()
            answers = result.answers
            user = result.user
            try:
                email_status = send_results_email(answers, user.email)
                if email_status != "Email sent successfully":
                    raise Exception(email_status)
            except Exception as e:
                transaction.set_rollback(True)
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'detail': 'Result saved and email sent'}, status=status.HTTP_201_CREATED)
    

#GET AND DELETE A SPECIFIC RESULT
class ResultDetailView(APIView):
    def get(self, request, id):
        result = get_object_or_404(Result, id=id)
        serializer = ResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        result = get_object_or_404(Result, id=id)
        result.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# RESOURCES MODEL

# CREATE AND LIST RESOURCES
class ResourceListView(APIView):
    def post(self, request):
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Resource created successfully.", "resource": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET, UPDATE AND DELETE SPECIFIC RESOURCE BY ID
class ResourceDetailAPIView(APIView):
    def get(self, request, resource_id):
        resources= get_object_or_404(Resource, resource_id=resource_id)
        serializer = ResourceSerializer(resources)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, resource_id):
        resources = get_object_or_404(Resource, resource_id=resource_id)
        serializer = ResourceSerializer(resources, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, resource_id):
        resources = get_object_or_404(Resource, resource_id=resource_id)
        resources.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ResourceSearchView(APIView):
    def get(self, request):
        activities = request.query_params.get('activities', None)
        if activities:
            resources = Resource.objects.filter(activities__icontains=activities)
            serializer = ResourceSerializer(resources, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "activities parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

# USER MODEL
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            group_permissions = Permission.objects.filter(group__user=user).values_list('codename', flat=True)
            user_permissions = user.user_permissions.values_list('codename', flat=True)
            all_permissions = set(group_permissions) | set(user_permissions)

            
            response_data = {
                "user": serializer.data,
                "permissions": list(all_permissions)
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDataMixin:
    def get_user_data(self, user):
        group_permissions = Permission.objects.filter(group__user=user).values_list('codename', flat=True)
        user_permissions = user.user_permissions.values_list('codename', flat=True)
        all_permissions = set(group_permissions)
        all_permissions.update(user_permissions)
        return {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
            'permissions': list(all_permissions) 
        }

class UserProfile(UserDataMixin, APIView):
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, user_id=user_id)
        user.refresh_from_db()
        user_data = self.get_user_data(user)
        return Response(user_data)
    
class UserListView(UserDataMixin, APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        user_data_list = [self.get_user_data(user) for user in users]
        return Response(user_data_list)