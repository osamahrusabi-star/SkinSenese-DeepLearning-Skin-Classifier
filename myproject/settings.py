"""
Django settings for myproject project.
"""

from pathlib import Path
import os

# === BASE SETUP ===
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-k=@tg4u1(8k5e_h+c*r3%ceg=4jip329og#w)&+p&z45e%#3(@'
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'testserver',  # For Django test client
]

# === INSTALLED APPS ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'skinsense',  # ✅ your main app
]

# === MIDDLEWARE ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ✅ handles login sessions
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ✅ required for auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

# === TEMPLATES ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ✅ correct template path
        'DIRS': [BASE_DIR / 'skinsense' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # ✅ needed for auth/session
                'django.contrib.auth.context_processors.auth',  # ✅ enables {{ user }}
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# === DATABASE ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skinsense_db',
        'USER': 'root',
        'PASSWORD': 'OSAMAh123@',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# === PASSWORD VALIDATORS ===
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

# === STATIC FILES ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'skinsense' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# === CSRF & SESSION CONFIG ===
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# ✅ Allow session cookies locally (not secure but fine for dev)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# ✅ Allow cookies to work across localhost/127.0.0.1 in dev
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# ✅ Ensure sessions stored in DB
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ✅ Keep user logged in even if browser closes (optional)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ✅ Ensure cookies have proper names (optional clarity)
CSRF_COOKIE_NAME = "csrftoken"
SESSION_COOKIE_NAME = "sessionid"

# === LANGUAGE & TIMEZONE ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# === DEFAULT AUTO FIELD ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# === SESSION & COOKIE CONFIGURATION ===

# ✅ Use the database backend for sessions (safest and default)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ✅ Cookie security (off for local dev)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ✅ Allow cookies across localhost / 127.0.0.1
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# ✅ Optional but useful clarity
SESSION_COOKIE_NAME = 'sessionid'
CSRF_COOKIE_NAME = 'csrftoken'

# ✅ Keep users logged in even after browser closes (optional)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ✅ Explicitly trusted origins
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

