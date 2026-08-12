from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-event-management-system"

DEBUG = True

ALLOWED_HOSTS = []


# --------------------------------------------------
# Applications
# --------------------------------------------------

INSTALLED_APPS = [
    # Third Party
    "crispy_forms",
    "crispy_bootstrap5",

    # Local Apps
    "core",
    "accounts",
    "events",
    "registrations",
    "dashboard",
    "notifications",

    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# --------------------------------------------------
# Middleware
# --------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# --------------------------------------------------
# Templates
# --------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notifications.context_processors.notification_context",
                'core.context_processors.dashboard_context',
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --------------------------------------------------
# Password Validation
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --------------------------------------------------
# Internationalization
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# Static Files
# --------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# --------------------------------------------------
# Media Files
# --------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# --------------------------------------------------
# Authentication
# --------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "dashboard_home"

LOGOUT_REDIRECT_URL = "home"


# --------------------------------------------------
# Crispy Forms
# --------------------------------------------------

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


# --------------------------------------------------
# Email Configuration
# --------------------------------------------------
# Development:
# Emails are printed in the terminal.
# No SMTP setup is required while developing.

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = "Event Management System <noreply@eventsystem.com>"

SERVER_EMAIL = DEFAULT_FROM_EMAIL


# --------------------------------------------------
# Production SMTP Example
# --------------------------------------------------
# Replace the values below and comment out the
# console backend above when deploying.

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "your_email@gmail.com"
# EMAIL_HOST_PASSWORD = "your_app_password"
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# --------------------------------------------------
# Security (Production)
# --------------------------------------------------

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"