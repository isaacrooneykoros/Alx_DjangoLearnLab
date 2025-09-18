"""
Django settings for LibraryProject project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔑 SECURITY
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-yuki__jf0cy+dgnvyhql^$!^r+h2$ita**68qpnil7tk5oiq1y"  # fallback for dev
)

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() == "true"  # default True for local
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# ✅ Cookies & Browser protections
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = not DEBUG
SECURE_BROWSER_XSS_FILTER = not DEBUG
X_FRAME_OPTIONS = "SAMEORIGIN" if DEBUG else "DENY"  # allow admin previews in dev

# ✅ HTTPS settings (only in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# 📦 Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'accounts',
    'bookshelf',

    # Third-party
    'csp',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

# ⚙️ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# 🔒 Content Security Policy (CSP)
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "style-src": ("'self'", "https://fonts.googleapis.com"),
        "script-src": ("'self'",),
        "font-src": ("'self'", "https://fonts.gstatic.com"),
    }
}

# 🗄 Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔑 Password validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🔐 Auth redirects
LOGIN_REDIRECT_URL = '/books/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# 📁 Static & Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 🔑 Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
