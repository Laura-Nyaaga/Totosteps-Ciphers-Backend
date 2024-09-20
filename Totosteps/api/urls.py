from django.urls import path
from .views import (
    AutismImageDetailListView, 
    AutismResultDetailListView, 
    AutismResultListView, 
    AutismImageListView,
    ChildListView,
    ChildDetailView
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
]
