import logging
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

# Set up logging
logger = logging.getLogger(__name__)

# Initialize OAuth
oauth = OAuth()
def callback(request):
    """
    Handle the OAuth callback and process user authentication.
    """
    
    try:
        # Authorize the access token using OAuth
        token = oauth.auth0.authorize_access_token(request)
        logger.info('Successfully authorized access token.')
        # Parse the ID token to get user information
        user_info = oauth.auth0.parse_id_token(request, token)
        logger.info('User information retrieved: %s', user_info)
        # Save user information in the session
        request.session['user'] = user_info
        logger.info('User information saved in session.')
        # Redirect to the profile page
        return redirect('/profile/')
    
    
    except Exception as e:
        # Log any errors that occur
        logger.error('Error processing OAuth callback: %s', str(e))
        # Redirect to an error page or handle the error as needed
        return redirect('/error/')
  
