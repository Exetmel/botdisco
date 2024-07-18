import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # ... existing apps ...
    'django.contrib.staticfiles',
    # ... existing apps ...
]

MIDDLEWARE = [
    # ... existing middleware ...
]

ROOT_URLCONF = 'your_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [BASE_DIR / 'jinja2'],
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                'django_jinja.builtins.extensions.DjangoStatic',
                'django_jinja.builtins.extensions.DjangoFiltersExtension',
            ],
        },
    },
]


WSGI_APPLICATION = 'your_project.wsgi.application'

# Database
DATABASES = {
    'default': env.db(),
}


INSTALLED_APPS = [
    # ... existing apps ...
    'django.contrib.staticfiles',
    # ... existing apps ...
    
]
STATIC_URL = '/static/'
STATICFILES_DIRS =[ BASE_DIR / 'static']
