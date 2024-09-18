import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.http import HttpResponse
from users.models import User
from django.http import JsonResponse, HttpResponseNotAllowed
from authlib.integrations.django_client import OAuth
from django.contrib.auth import authenticate



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


def login(request):
    if request.method == "POST":
        try:
            credentials = json.loads(request.body)
            email = credentials.get("email")
            password = credentials.get("password")
            
            # Redirect to OAuth provider for authentication
            auth_url = "https://localhost:8000/authorize"
            redirect_uri = request.build_absolute_uri(reverse("callback"))
            client_id = settings.OAUTH_CLIENT_ID
            scope = "openid profile email"
            auth_url_with_params = f"{auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
            
            return redirect(auth_url_with_params)
        
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return JsonResponse({"error": f"Login failed: {str(e)}"}, status=401)
    
    elif request.method == "GET":
        return render(request, "authentication/index.html")
    
    else:
        return HttpResponseNotAllowed(["POST", "GET"])


import requests

def callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({"error": "Authorization code not found."}, status=400)
    
    try:
        token_url = "http://localhost:8000/token"
        response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': request.build_absolute_uri(reverse("callback")),
            'client_id': settings.OAUTH_CLIENT_ID,
            'client_secret': settings.OAUTH_CLIENT_SECRET
        })
        
        tokens = response.json()
        
        if response.status_code == 200:
            return JsonResponse({"message": "Successfully authenticated", "tokens": tokens}, status=200)
        else:
            return JsonResponse({"error": "Failed to authenticate"}, status=response.status_code)
    
    except Exception as e:
        print(f"Error during callback: {str(e)}")
        return JsonResponse({"error": f"Callback failed: {str(e)}"}, status=500)




def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )
    
def check_existing_email(email):
    return User.objects.filter(email=email).exists()

def index(request):
    user = request.session.get("user")
    if not user:
        return redirect(reverse("login"))
    email = user['userinfo']['email']
    if not email:
        return HttpResponse("email not passed in the")
    if not check_existing_email(email):
        return HttpResponse("user does not exist")
    return render(
        request,
        "authentication/index.html",
        context={
            "session": user,
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )