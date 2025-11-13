from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Prácticas de seguridad desactivadas temporalmente.

# import os
# from dotenv import load_dotenv

# load_dotenv(BASE_DIR / ".env")

# SECRET_KEY = os.getenv("SECRET_KEY", "insecure-default-key")
# DEBUG = os.getenv("DEBUG", "False").lower() == "true"
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

SECRET_KEY='django-insecure-5rl8yxb!#rh*ohpe-3hz($#9riec0xd=eq^ugwh=+_5aumw4l8'
DEBUG=True
ALLOWED_HOSTS=['localhost','127.0.0.1']

#

INSTALLED_APPS = [
    'register_par.apps.RegisterParConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions'
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

ROOT_URLCONF = 'olimpi_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'olimpi_app.wsgi.application'

# Prácticas de seguridad desactivadas temporalmente.

'''
DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        'USER': os.getenv("DB_USER", ""),
        'PASSWORD': os.getenv("DB_PASS", ""),
        'HOST': os.getenv("DB_HOST", ""),
        'PORT': os.getenv("DB_PORT", ""),
    }
}
'''

#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'