from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib import messages
from user.models import User
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Django's built-in authentication
        if user is not None:
            django_login(request, user)
            return redirect(reverse("index"))  # Redirect to index or dashboard
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'authentication/login.html')
def sso_login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    userinfo = oauth.auth0.parse_id_token(request, token)
    request.session["user"] = userinfo
    email = userinfo.get("email")
    # If the user exists in the local database, log them in
    if check_existing_email(email):
        user = User.objects.get(email=email)
        django_login(request, user)  # Log the user in via Django's session system
    return redirect(reverse("index"))
def logout_view(request):
    django_logout(request)  # Logout from Django session
    request.session.clear()  # Clear Auth0 session if any
    return redirect(reverse("login_view"))  # Redirect to login
def check_existing_email(email):
    return User.objects.filter(email=email).exists()
@login_required
def index(request):
    if request.user.is_authenticated:
        return render(
            request,
            "authentication/index.html",
            context={"session": request.session.get("user", {}), "pretty": json.dumps(request.session.get("user", {}), indent=4)},
        )
    else:
        return HttpResponse("User is not registered.")






