"""
Django settings for LMNOPsite project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8c01$#j44g3znb)$q0()8)!%ts-jc)k12!a75-!63qb%bj=d4k'

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lmn',
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

ROOT_URLCONF = 'lmnop_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'lmnop_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if os.getenv('GAE_INSTANCE'):
    DATABASES = {

        # Uncomment this when you are ready to use Postgres.
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'lmnop',
            'USER': 'lmnop',
            'PASSWORD': os.environ['LMNOP_DB_PW'],
            'HOST': '/cloudsql/lmnop-271010:us-central1:lmnop-new',
            'PORT': '5432'
        }
        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': 'lmnop.sqlite',
        # }
    }

else:
    # DATABASES['default']['HOST'] = '127.0.0.1'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'lmnop',
            'USER': 'lmnop',
            'PASSWORD': os.environ['LMNOP_DB_PW'],
            'HOST': '127.0.0.1',
            'PORT': '5432'
        }
    }
    

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'www', 'static')

# Where to send user after successful login if no other page is provided.
# Should provide the user object.
LOGIN_REDIRECT_URL = 'lmn:my_user_profile'
''' Commented out so the logout process usess the URL on lmn/urls.py,
LOGOUT_REDIRECT_URL = 'lmn:homepage'
'''

# MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if os.getenv('GAE_INSTANCE'):
    GS_STATIC_FILE_BUCKET = 'lmnop-271010.appspot.com'

    STATIC_URL = f'https://storage.cloud.google.com/{GS_STATIC_FILE_BUCKET}/static/'

    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = 'user-notes-pics'
    MEDIA_URL = f'https://storage.cloud.google.com/{GS_BUCKET_NAME}/media/'

    from google.oauth2 import service_account

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file('lmnop-271010-credentials.json')

else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
