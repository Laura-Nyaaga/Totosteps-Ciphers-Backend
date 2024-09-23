from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from assessment.models import Assessment
from child.models import Child
from milestones.models import Milestone
from resources.models import Resource
from result.models import Result
from django.db.models import Sum, Avg
from result.utils import send_results_email
from .serializers import AssessmentSerializer, ChildSerializer, MilestoneSerializer, ResourceSerializer, ResultSerializer
from autism_results.models import Autism_Results
from autism_image.models import Autism_Image
from .serializers import AutismImageSerializer, AutismResultsSerializer





class UserDetailView(APIView):
    # This APIView is to show the detailed information about the User
    
    def get(self, request, id):
 #This is for getting a specific user by using their unique id
    
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# This is for getting a list of all users:
class UserListView(APIView):

    def get(self, request):
        """
        Handles GET requests to retrieve a list of users.
        """
        users = User.objects.all() 
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

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
    def get(self, request, milestone_id):
        milestone = get_object_or_404(Milestone, milestone_id=milestone_id)
        serializer = MilestoneSerializer(milestone)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, milestone_id):
        question = get_object_or_404(Milestone, milestone_id=milestone_id)
        serializer = MilestoneSerializer(question, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, milestone_id):
        question = get_object_or_404(Milestone, milestone_id=milestone_id)
        question.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# CHILD CURRENT MILESTONE
class ChildMilestoneListView(APIView):
    def get(self, request, child_id):
        child = get_object_or_404(Child, child_id=child_id)
        child_age_in_months = child.get_age_in_months()
        current_milestone = Milestone.get_current_milestone(child_age_in_months)
        milestones = Milestone.objects.all().order_by('age')  
        milestone_data = []
        for milestone in milestones:
            is_current = (milestone == current_milestone)
            milestone_data.append({
                "id": milestone.id,
                "age": milestone.age_range,
                "description": milestone.description,
                "summary": milestone.summary,
                "is_current": is_current  
            })
        return Response(milestone_data, status=200)

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
    def post(self, request):
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            answers = result.answers
            parent_email = request.data.get('parent_email')  # Get the parent email from the request

            if parent_email:
                email_status = send_results_email(answers, parent_email)  # Send the email to the parent email

                if email_status == "Email sent successfully":
                    return Response({'detail': 'Result saved and email sent'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': email_status}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'error': 'Parent email not provided'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
