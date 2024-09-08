from django.urls import path
from . import views

"""
 This module defines the URL patterns for the authentication-related views.
- The `index` view is mapped to the root URL ("").
 - The `login` view handles user login and redirects them to the Auth0 authentication page.
 - The `logout` view logs the user out and redirects them to the Auth0 logout endpoint.
- The `callback` view processes the authentication response from Auth0 and handles user session management.
"""

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
]