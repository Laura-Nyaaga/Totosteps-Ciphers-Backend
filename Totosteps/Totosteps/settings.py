
from pathlib import Path
import os
from dotenv import load_dotenv,find_dotenv
from datetime import timedelta
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")


SECRET_KEY = 'django-insecure-xw(pvf+anx%9uziaecv^uwp41mkwj1g2p@l#5t@h!8hh@4_ky6'

DEBUG = True

ALLOWED_HOSTS = ['localhost']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'authentication',
    'assesment_history_results',
    'assesment_questions',
    'users',
    'child',
    'dashboard',
    'milestones',
    'Totosteps',
    'resources',
    'rest_framework',
    'rest_framework_simplejwt',

]


AUTHENTICATION_BACKENDS = [
'authlib.integrations.django_client.AuthBackend',
'django.contrib.auth.backends.ModelBackend',
'path.to.Auth0Backend',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
        'NAME':'totosteps_database',
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

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")

AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

REDIRECT_URI = 'http://127.0.0.1:8000/auth/callback/'
REDIRECT_URI = 'http://127.0.0.1:8000/auth/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365*10),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365*10),  
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

