import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from users.models import User

# Initialize OAuth client
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"http://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    """
    Redirect the user to the Auth0 login page.
    """
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    """
    Handle the callback from Auth0 after user authentication.
    """
    # Exchange authorization code for an access token
    token = oauth.auth0.authorize_access_token(request)
    # Store token in session
    request.session["user"] = token
    # Redirect to the index page
    return redirect(request.build_absolute_uri(reverse("index")))

def logout(request):
    """
    Log the user out by clearing the session and redirecting to Auth0 logout URL.
    """
    # Clear the session data
    request.session.clear()
    # Build the Auth0 logout URL
    auth0_logout_url = (
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )
    # Redirect to Auth0's logout URL
    return redirect(auth0_logout_url)

def check_existing_email(email):
    """
    Check if a user with the given email address already exists.
    """
    return User.objects.filter(email=email).exists()

def index(request):
    """
    Render the index page if the user is logged in; otherwise, redirect to login.
    """
    user = request.session.get("user")
    if not user:
        return redirect(reverse("login"))
    email = user['userinfo'].get('email')
    if not email:
        return HttpResponse("Email not passed in the token.")
    if not check_existing_email(email):
        return HttpResponse("User does not exist.")


    # Render the index page with user session data
    return render(
        request,
        "login/index.html",
        context={
            "session": user,
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )