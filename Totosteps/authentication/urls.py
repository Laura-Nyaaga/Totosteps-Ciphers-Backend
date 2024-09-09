from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login_view"),
    path("sso-login", views.sso_login, name="sso_login"),
    path("logout", views.logout_view, name="logout_view"),
    path("callback", views.callback, name="callback"),
]