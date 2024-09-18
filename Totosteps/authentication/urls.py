
# urls.py
from django.urls import path
from .views import login, callback, logout, index

urlpatterns = [
    path('api/users/login/', login, name='login'),        
    path('api/users/callback/', callback, name='callback'),   ]
