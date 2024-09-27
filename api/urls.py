from django.urls import path
from .views import (
    AssessmentDetailView,
    AssessmentListView,
    AutismImageUploadView, 
    AutismResultDetailListView, 
    AutismResultListView, 
    CategoryQuestionsListView,
    ChildListView,
    ChildDetailView,
    ChildMilestoneListView,
    MilestoneDetailView,
    MilestoneListView,
    MilestoneQuestionsListView,
    ParentDetailview,
    ParentListView,
    RegisterView,
    ResourceDetailAPIView,
    ResourceListView,
    ResourceSearchView,
    RestoreUserView,
    RestrictUserView,
    ResultDetailView,
    ResultListView,
    UserListView,
    UserProfile
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Autism-related paths
    path('results/<int:image_id>/', AutismResultDetailListView.as_view(), name='autism-result-detail'), 
    path('results/', AutismResultListView.as_view(), name='autism-result-list'),
    path('results/<int:image_id>/', AutismResultDetailListView.as_view(), name='autism-result-detail'),
    path('upload/', AutismImageUploadView.as_view(), name='image-upload'), 

    # Child-related paths
    path('children/', ChildListView.as_view(), name='child-list'),
    path('children/<int:child_id>/', ChildDetailView.as_view(), name='child-detail'),

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
    
    # REGISTER MODEL
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='all_users'),  
    path('user-profile/<int:user_id>/', UserProfile.as_view(), name='user_profile'),
    path('users/<int:user_id>/restrict/', RestrictUserView.as_view(), name='user-restrict'),
    path('users/<int:user_id>/restore/', RestoreUserView.as_view(), name='user-restore'),

    # Parent View
    path('parent/', ParentListView.as_view(), name='parent-view'),
    path('parent/<int:user_id>/', ParentDetailview.as_view(), name='parent-detailview'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
