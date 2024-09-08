from django.urls import path
from .views import RegisterView, UserListView, UserDetailView

"""
This module defines the URL patterns for user-related API endpoints.
The `UserListView` is mapped to the 'users/' URL, which provides a list of all users.
The `RegisterView` is mapped to the 'register/' URL, which handles user registration.
The `UserDetailView` is mapped to 'users/<int:id>/', which provides endpoints
 for retrieving, updating, and deleting individual users by their ID.
 These paths connect the views to their respective endpoints in the application.
"""
urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
]