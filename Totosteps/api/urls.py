

from django.urls import path
from .views import  UserListView,UserDetailView,UserMetricsView, ResourceUsageView


urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('user-metrics/', UserMetricsView.as_view(), name='user-metrics'),
    path('resource-usage/', ResourceUsageView.as_view(), name='resource-usage'),
]