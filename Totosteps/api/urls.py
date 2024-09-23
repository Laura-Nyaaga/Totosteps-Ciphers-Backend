from django.urls import path
from .views import (
    AssessmentDetailView,
    AssessmentListView,
    AutismImageDetailListView, 
    AutismResultDetailListView, 
    AutismResultListView, 
    AutismImageListView,
    CategoryQuestionsListView,
    ChildListView,
    ChildDetailView,
    ChildMilestoneListView,
    MilestoneDetailView,
    MilestoneListView,
    MilestoneQuestionsListView,
    ResourceDetailAPIView,
    ResourceListView,
    ResourceSearchView,
    ResultDetailView,
    ResultListView,
    UserDetailView, 
    UserListView,
    Resource_Metrics
)

urlpatterns = [
    # Autism-related paths
    path('results/<int:image_id>/', AutismResultDetailListView.as_view(), name='autism-result-detail'), 
    path('results/', AutismResultListView.as_view(), name='autism-result-list'),  
    path('images/', AutismImageListView.as_view(), name='image-list'),  
    path('images/<int:image_id>/', AutismImageDetailListView.as_view(), name='image-details'),  

    # Child-related paths
    path('children/', ChildListView.as_view(), name='child-list'),
    path('children/<int:id>/', ChildDetailView.as_view(), name='child-detail'),

     # MILESTONE PATH
    path('milestones/', MilestoneListView.as_view(), name='milestone-list'),
    path('milestones/<int:milestone_id>/', MilestoneDetailView.as_view(), name='milestone-detail'),
    path('milestones/<int:milestone_id>/questions/', MilestoneQuestionsListView.as_view(), name='milestone-questions'),

     # CHILDMILESTONE
    path('child/<int:child_id>/milestones/', ChildMilestoneListView.as_view(), name='child_milestones'),

     # ASSESSMENT PATH
    path('assessment/', AssessmentListView.as_view(), name='assessment_create'),
    path('assessment/<int:question_id>/', AssessmentDetailView.as_view(), name='get_question_by_id'),
    path('assessment/all/', AssessmentListView.as_view(), name='list_all_questions'),
    path('questions/category/<str:category>/', CategoryQuestionsListView.as_view(), name='category-questions-list'),

    # RESULT PATH
    path('result/', ResultListView.as_view(), name='create-result'),
    path('result/<int:id>/', ResultDetailView.as_view(), name='get-result'),

     # RESOURCES PATH
    path('resources/', ResourceListView.as_view(), name='resource-list'),
    path('resources/<int:resource_id>/', ResourceDetailAPIView.as_view(), name='resource-detail'),
    path('resources/search/', ResourceSearchView.as_view(), name='resource-search'),
    
    #DASHBOARD-METRICS PATH
    path('users/<int:id>/', UserDetailView.as_view()),  # User detail by ID
    path('users/', UserListView.as_view()),         # List of all users 
    path('resource_metrics/', Resource_Metrics.as_view()),  # Resource usage metrics
    
]
