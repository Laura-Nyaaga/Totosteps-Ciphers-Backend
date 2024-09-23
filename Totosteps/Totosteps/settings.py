
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-xw(pvf+anx%9uziaecv^uwp41mkwj1g2p@l#5t@h!8hh@4_ky6'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autism_image',
    'autism_results',
    'child',
    'api',
    'rest_framework',
    'result',
    'assessment',
    'milestones',
    'resources',
    'users',
    # 'rest_framework_simplejwt.token_blacklist',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Totosteps.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR,'My App', 'templates')


# settings.py
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allows unrestricted access to all views
    ]
}

SIMPLE_JWT = {
   'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
   'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates',TEMPLATE_DIR)],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'Totosteps.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Totostep <totostepsciphers@gmail.com>')

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.SessionAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

# SIMPLE_JWT = {
#     'AUTH_COOKIE': 'access_token',  # Cookie name for storing the access token
#     'AUTH_COOKIE_SECURE': False,    # Set to True in production
#     'AUTH_COOKIE_HTTP_ONLY': True,  # HTTP-only cookie to prevent JavaScript access
#     'AUTH_COOKIE_PATH': '/',        # Cookie available site-wide
#     'AUTH_COOKIE_SAMESITE': 'Lax',  # Adjust SameSite settings as needed
# }

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")


REDIRECT_URI= "http://127.0.0.1:8000/auth/callback"