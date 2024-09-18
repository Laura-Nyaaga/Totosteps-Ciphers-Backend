from django.urls import path
from .views import UserListView, UserDetailView, RegisterView, LoginView, LogoutView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),  # GET: List all users, POST: Create new user (authenticated user)
    path('users/register/', RegisterView.as_view(), name='register'),  # POST: User registration
    path('users/login/', LoginView.as_view(), name='login'),  # POST: User login
    path('users/logout/', LogoutView.as_view(), name='logout'),  # POST: User logout
    path('users/profile/', UserProfileView.as_view(), name='user_profile'),  # GET, PUT: User profile
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
]
