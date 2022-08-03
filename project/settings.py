"""
Django settings for project project.

Generated by "django-admin startproject" using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

# standard library
import os
import sys

from pathlib import Path

# django
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / "subdir".
PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False) == "True"

# WARNING: do not make your code depend on this value
TEST = False

ALLOWED_HOSTS = [
    os.environ.get("ALLOWED_HOST", ""),
    "localhost",
    "127.0.0.1",
]

SITE_ID = 1

# TEST should be true if we are running python tests
TEST = "test" in sys.argv or "pytest" in sys.argv[0]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # extensions
    "django_extensions",
    # required apps
    "base.apps.BaseConfig",
    "users",
    # external
    "loginas",
    "webpack_loader",
    # internal
    "parameters",
    "regions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "base.middleware.RequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.tz",
                "django.template.context_processors.i18n",
            ],
            "loaders": [
                (
                    "pypugjs.ext.django.Loader",
                    (
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ),
                )
            ],
            "builtins": [
                "pypugjs.ext.django.templatetags",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE"),
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("PGPASSWORD"),
        "HOST": os.environ.get("PGHOST", "127.0.0.1"),
        "PORT": os.environ.get("PGPORT", "5432"),
        "DISABLE_SERVER_SIDE_CURSORS": (
            os.environ.get("POSTGRES_DISABLE_SERVER_SIDE_CURSORS", False) == "True"
        ),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
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

AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "es"

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    PROJECT_DIR / "locale",
    BASE_DIR / "assets" / "locale",
]

# Email
ENABLE_EMAILS = os.environ.get("ENABLE_EMAILS", False) == "True"
if DEBUG or not ENABLE_EMAILS:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("SMTP_HOST", None)
EMAIL_PORT = int(os.environ.get("SMTP_PORT", 587))
EMAIL_HOST_USER = os.environ.get("SMTP_USER", None)
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", None)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")
EMAIL_SENDER_NAME = os.environ.get("EMAIL_SENDER_NAME", "Sender Name")

# Credentials for AWS services
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if not DEBUG:
    STATICFILES_DIRS = [
        # Webpack bundles
        ("bundles", BASE_DIR / "assets/bundles"),
    ]

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", None)
if AWS_STORAGE_BUCKET_NAME:
    # Store static and media in S3 or DigitalOcean spaces.
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    # Note: this applies to static files only
    # (specifically to storages with `default_acl="public-read"` only)

    DO_SPACES_REGION = os.environ.get("DO_SPACES_REGION", None)
    DO_SPACES_CDN_ENABLED = False

    if DO_SPACES_REGION:
        AWS_S3_ENDPOINT_URL = f"https://{DO_SPACES_REGION}.digitaloceanspaces.com"
        DO_SPACES_CDN_ENABLED = (
            os.environ.get("DO_SPACES_CDN_ENABLED", "True") == "True"
        )

    STATICFILES_STORAGE = "project.storage_backends.S3StaticStorage"
    DEFAULT_FILE_STORAGE = "project.storage_backends.S3MediaStorage"

else:
    STATIC_ROOT = PROJECT_DIR / "static"
    STATIC_URL = "/static/"

    MEDIA_ROOT = PROJECT_DIR / "media"
    MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# google analytics
GOOGLE_ANALYTICS_CODE = os.environ.get("GOOGLE_ANALYTICS_CODE", "")

# recaptcha
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY", "")

# loginas
CAN_LOGIN_AS = "base.utils.can_loginas"
LOGOUT_URL = reverse_lazy("loginas-logout")
LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy("admin:index")

# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            # No 'filters', to log even when DEBUG=False
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# The change's information of this fields will be ignored in the logs
LOG_SENSITIVE_FIELDS = [
    "password",
]

# These fields will be ignored in the logs
LOG_IGNORE_FIELDS = [
    "created_at",
    "updated_at",
    "original_dict",
    "id",
    "date_joined",
]

# Cache
# https://docs.djangoproject.com/en/3.2/topics/cache/#setting-up-the-cache

if not DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": os.environ.get("MEMCACHED_LOCATION"),
        }
    }

# Django Webpack Loader
# https://github.com/django-webpack/django-webpack-loader#configuring-the-settings-file

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": False,
        "BUNDLE_DIR_NAME": "bundles/",
        "STATS_FILE": BASE_DIR / "webpack-stats.json",
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": 1,  # 1 second timeout for webpack compilation
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

# HTTPS
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-proxy-ssl-header

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# This assumes the provided nginx is always before django. It contains:
# "proxy_set_header X-Forwarded-Proto $scheme;"

# HSTS added by Django. This is redundant because nginx adds it as well,
# but it silences deploy check warnings.
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = not DEBUG
# Requests are redirected by nginx, but setting this here silences a warning.

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
