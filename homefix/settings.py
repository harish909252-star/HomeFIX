import os
from pathlib import Path
import dj_database_url


# =====================================
# BASE DIRECTORY
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================
# SECURITY SETTINGS
# =====================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-local-development-key"
)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

# Render hostname
RENDER_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

if RENDER_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_HOSTNAME)

# Additional allowed hosts
EXTRA_HOSTS = os.getenv("ALLOWED_HOSTS", "")

if EXTRA_HOSTS:
    ALLOWED_HOSTS.extend(
        host.strip()
        for host in EXTRA_HOSTS.split(",")
        if host.strip()
    )


# =====================================
# CSRF SETTINGS
# =====================================

CSRF_TRUSTED_ORIGINS = []

if RENDER_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(
        f"https://{RENDER_HOSTNAME}"
    )


# =====================================
# INSTALLED APPS
# =====================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "services",
]


# =====================================
# MIDDLEWARE
# =====================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =====================================
# URL CONFIGURATION
# =====================================

ROOT_URLCONF = "homefix.urls"


# =====================================
# TEMPLATES
# =====================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",

                "django.contrib.auth.context_processors.auth",

                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =====================================
# WSGI APPLICATION
# =====================================

WSGI_APPLICATION = "homefix.wsgi.application"


# =====================================
# DATABASE CONFIGURATION
# PostgreSQL on Render
# SQLite on Local Computer
# =====================================

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:

    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }

else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =====================================
# PASSWORD VALIDATION
# =====================================

AUTH_PASSWORD_VALIDATORS = []


# =====================================
# LANGUAGE & TIME ZONE
# =====================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =====================================
# STATIC FILES
# =====================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# =====================================
# WHITENOISE CONFIGURATION
# =====================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# =====================================
# DEFAULT PRIMARY KEY
# =====================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =====================================
# TWILIO WHATSAPP SETTINGS
# =====================================

TWILIO_ACCOUNT_SID = os.getenv(
    "TWILIO_ACCOUNT_SID", ""
)

TWILIO_AUTH_TOKEN = os.getenv(
    "TWILIO_AUTH_TOKEN", ""
)

TWILIO_WHATSAPP_FROM = os.getenv(
    "TWILIO_WHATSAPP_FROM", ""
)


# =====================================
# SECURITY COOKIES
# =====================================

CSRF_COOKIE_SECURE = not DEBUG

SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_HTTPONLY = False

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)