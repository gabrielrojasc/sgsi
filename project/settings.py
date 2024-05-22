"""
Django settings for newproj project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import ast
import os

from datetime import timedelta
from importlib.util import find_spec
from pathlib import Path

from django.contrib.messages import constants as messages
from django.urls import reverse_lazy

from celery.schedules import crontab


def get_env_value(key, default, default_if_blank=False):
    try:
        value = os.environ[key].strip()
        if not value and default_if_blank:
            return default
    except KeyError:
        return default
    else:
        return value


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as error:
            msg = f"{value} is an invalid value for {name}"
            raise ValueError(msg) from error
    return default_value


SILENCED_SYSTEM_CHECKS = []


# Build paths inside the project like this: BASE_DIR / "subdir".
PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env("DEBUG", False)
# Also don't turn this on in a server, use the proper deployment instead!
LOCAL_PROD_TESTING = get_bool_from_env("LOCAL_PROD_TESTING", False)

ENVIRONMENT_NAME = get_env_value(
    "ENVIRONMENT_NAME",
    "Please define ENVIRONMENT_NAME",
    default_if_blank=True,
)

# WARNING: do not make your code depend on this value
TEST = False

# Please edit test_settings to define your ignored namespaces
URLS_TEST_IGNORED_NAMESPACES = []

TEST_RUNNER = "project.test_runner.PytestTestRunner"

ALLOWED_HOSTS = [
    os.environ.get("ALLOWED_HOST", ""),
    "localhost",
    "127.0.0.1",
]

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    # This app first so it correctly overrides runserver command from staticfiles:
    "base.apps.BaseConfig",
    "base.apps.BaseAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # required apps
    "users.apps.UsersConfig",
    # external
    "loginas",
    "api_client",
    "django_vite",
    "django_celery_beat",
    "rest_framework",
    "django_recaptcha",
    "social_django",
    # internal
    "parameters.apps.ParametersConfig",
    "regions.apps.RegionsConfig",
    "documents.apps.DocumentsConfig",
    "information_assets.apps.InformationAssetsConfig",
    "risks.apps.RisksConfig",
    "processes.apps.ProcessesConfig",
]

MIDDLEWARE = [
    "base.middleware.ReadinessCheckMiddleware",
    "xff.middleware.XForwardedForMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "base.middleware.RequestMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if find_spec("debug_toolbar"):
    ENABLE_DEBUG_TOOLBAR = DEBUG and get_bool_from_env("ENABLE_DEBUG_TOOLBAR", False)
else:
    ENABLE_DEBUG_TOOLBAR = False

if ENABLE_DEBUG_TOOLBAR:
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append(
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]

if find_spec("django_extensions"):
    ENABLE_DJANGO_EXTENSIONS = get_bool_from_env("ENABLE_DJANGO_EXTENSIONS", False)
else:
    ENABLE_DJANGO_EXTENSIONS = False

if ENABLE_DJANGO_EXTENSIONS:
    INSTALLED_APPS.append("django_extensions")

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.tz",
                "django.template.context_processors.i18n",
                "base.context_processors.build_info",
                "base.context_processors.react_context",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_ROUTERS = ["api_client.db_router.ClientLogDbRouter"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE"),
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("PGPASSWORD"),
        "HOST": os.environ.get("PGHOST", "127.0.0.1"),
        "PORT": os.environ.get("PGPORT", "5432"),
        "DISABLE_SERVER_SIDE_CURSORS": (
            get_bool_from_env("POSTGRES_DISABLE_SERVER_SIDE_CURSORS", False)
        ),
    },
    "logs": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": f"{os.environ.get('PGDATABASE')}-logs",
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("PGPASSWORD"),
        "HOST": os.environ.get("PGHOST", "127.0.0.1"),
        "PORT": os.environ.get("PGPORT", "5432"),
        "DISABLE_SERVER_SIDE_CURSORS": (
            get_bool_from_env("POSTGRES_DISABLE_SERVER_SIDE_CURSORS", False)
        ),
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
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
DEFAULT_GROUP_NAME = "Employee"
USER_REGISTRATION_ENABLED = False

DJANGO_AUTH_ENABLED = get_bool_from_env("DJANGO_AUTH_ENABLED", True)
GOOGLE_OAUTH_ENABLED = get_bool_from_env("GOOGLE_OAUTH_ENABLED", False)

AUTHENTICATION_BACKENDS = []
if DJANGO_AUTH_ENABLED:
    AUTHENTICATION_BACKENDS.append("django.contrib.auth.backends.ModelBackend")
if GOOGLE_OAUTH_ENABLED:
    AUTHENTICATION_BACKENDS.append("social_core.backends.google.GoogleOAuth2")
    AUTHENTICATION_BACKENDS.append("social_core.backends.google.GoogleOAuth")

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en"
FAKER_LOCALES = ["es_CL"]

TIME_ZONE = "America/Santiago"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    PROJECT_DIR / "locale",
    BASE_DIR / "assets" / "locale",
]

# Email
ENABLE_EMAILS = get_bool_from_env("ENABLE_EMAILS", False)
if DEBUG or not ENABLE_EMAILS:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("SMTP_HOST", None)
EMAIL_PORT = int(os.environ.get("SMTP_PORT", 587))
EMAIL_HOST_USER = os.environ.get("SMTP_USER", None)
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD", None)
DEFAULT_FROM_EMAIL = get_env_value(
    "DEFAULT_FROM_EMAIL",
    "webmaster@localhost",
    default_if_blank=True,
)
EMAIL_SENDER_NAME = get_env_value(
    "EMAIL_SENDER_NAME",
    "Sender Name",
    default_if_blank=True,
)

# Credentials for AWS services
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)


# https://github.com/MrBin99/django-vite
VITE_DEV_MODE = get_bool_from_env("VITE_DEV_MODE", DEBUG)
DJANGO_VITE_ASSETS_PREFIX = BASE_DIR / "assets" / "bundles"
DJANGO_VITE_MANIFEST_FILE = os.environ.get("VITE_MANIFEST", "manifest.json")

DJANGO_VITE = {
    "default": {
        "dev_mode": VITE_DEV_MODE,
        "manifest_path": DJANGO_VITE_ASSETS_PREFIX / DJANGO_VITE_MANIFEST_FILE,
        "dev_server_port": 3000,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if not (DEBUG and VITE_DEV_MODE):
    STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PREFIX]

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", None)
if AWS_STORAGE_BUCKET_NAME:
    # Store static and media in S3 or DigitalOcean spaces.
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    # Note: this applies to static files only
    # (specifically to storages with `default_acl="public-read"` only)

    DO_SPACES_REGION = os.environ.get("DO_SPACES_REGION", None)
    DO_SPACES_CDN_ENABLED = False

    if DO_SPACES_REGION:
        AWS_S3_ENDPOINT_URL = f"https://{DO_SPACES_REGION}.digitaloceanspaces.com"
        DO_SPACES_CDN_ENABLED = get_bool_from_env("DO_SPACES_CDN_ENABLED", True)

    STORAGES = {
        "staticfiles": {
            "BACKEND": "project.storage_backends.S3StaticStorage",
        },
        "default": {
            "BACKEND": "project.storage_backends.S3MediaStorage",
        },
    }

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
RECAPTCHA_WIDGET = os.environ.get(
    "RECAPTCHA_WIDGET", "django_recaptcha.widgets.ReCaptchaV3"
)

# loginas
CAN_LOGIN_AS = "base.utils.can_loginas"
LOGOUT_URL = reverse_lazy("loginas-logout")
LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy("admin:index")

LOGOUT_REDIRECT_URL = reverse_lazy("home")
LOGIN_REDIRECT_URL = reverse_lazy("home")

# logging
debug_logs = DEBUG or LOCAL_PROD_TESTING

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
        "verbose": {
            "format": (
                "%(asctime)s %(levelname)s %(name)s %(message)s "
                "[PID:%(process)d:%(threadName)s]"
            ),
        },
        "app_logging": {
            "format": (
                "%(levelname)s %(asctime)s [%(name)s] %(message)s "
                "[PID:%(process)d:%(threadName)s]"
            ),
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "json": {
            "()": "project.logging.JsonFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(lineno)s %(message)s %(name)s "
                "%(pathname)s %(process)d %(threadName)s"
            ),
        },
        "celery_json": {
            "()": "project.logging.JsonCeleryFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(celeryTaskId)s %(celeryTaskName)s "
            ),
        },
        "celery_task_json": {
            "()": "project.logging.JsonCeleryTaskFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(celeryTaskId)s %(celeryTaskName)s "
                "%(message)s "
            ),
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if debug_logs else "json",
        },
        "app_logger": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "app_logging",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server" if debug_logs else "json",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "api_clients": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if debug_logs else "json",
        },
        "celery_app": {
            "level": "DEBUG" if debug_logs else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if debug_logs else "celery_json",
        },
        "celery_task": {
            "level": "DEBUG" if debug_logs else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if debug_logs else "celery_task_json",
        },
    },
    "loggers": {
        "": {
            # Catch-all to print "logger.info" to console
            # https://stackoverflow.com/a/70343506
            "handlers": ["default", "mail_admins"],
            "level": "INFO",
        },
        "users": {
            "handlers": ["app_logger"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "api_clients": {
            "handlers": ["api_clients"],
            "level": "ERROR",
            "propagate": False,
        },
        "celery.app.trace": {
            "handlers": ["celery_app"],
            "level": "DEBUG" if debug_logs else "INFO",
            "propagate": False,
        },
        "celery.task": {
            "handlers": ["celery_task"],
            "level": "DEBUG" if debug_logs else "INFO",
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
    "last_login",
]

# Cache
# https://docs.djangoproject.com/en/3.2/topics/cache/#setting-up-the-cache
if os.environ.get("CACHE_URL"):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ.get("CACHE_URL"),
        },
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        },
    }

# HTTPS
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-proxy-ssl-header

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# This assumes the provided nginx is always before django. It contains:
# "proxy_set_header X-Forwarded-Proto $scheme;"

# Get client IP at request.META.get('REMOTE_ADDR'), instead of 127.0.0.1 from nginx.
# Assumes a configuration like:
#   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
# See https://github.com/ferrix/xff/.
#
# The default value for .env is "1", a single nginx before django.
# Default to 0 on misconfiguration, to prevent header spoofing.
XFF_TRUSTED_PROXY_DEPTH = int(
    get_env_value("XFF_TRUSTED_PROXY_DEPTH", default=0, default_if_blank=True)
)
# Allow "curl localhost:8000" to succeed without X-Forwarded-For:
XFF_STRICT = False

# Set HSTS with nginx instead of django.
# Even if we set it with django, we still need to silence one warning
# (SECURE_HSTS_INCLUDE_SUBDOMAINS).
SECURE_HSTS_SECONDS = 0
SILENCED_SYSTEM_CHECKS.append("security.W004")

# Use this to know if the site is hosted with https or not.
# Has no real effect as requests are redirected by nginx (or another proxy)
# before django.
SECURE_SSL_REDIRECT = not DEBUG and not LOCAL_PROD_TESTING

# Disable "Secure" cookies to enable access from LAN over http
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT

# Celery settings
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or ""
CELERY_TASK_ALWAYS_EAGER = not CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", None)

# Celery beat schedules
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {
    "sample-scheduled-task-minutely": {
        "task": "base.tasks.sample_scheduled_task",
        "schedule": timedelta(seconds=60),
    },
    "monthly-api-logs-cleanup": {
        "task": "api_client.tasks.client_log_cleanup",
        "schedule": crontab(0, 0, day_of_month="1"),
    },
}
"""
More examples:
CELERY_BEAT_SCHEDULE = {
    "some-scheduled-task-1": {
        "task": "app.tasks.some_task",
        "schedule": timedelta(days=1),
    },
    "some-scheduled-task-2": {
        "task": "app.tasks.some_task",
        "schedule": crontab(hour=0, minute=0),
    },
    "some-scheduled-task-3": {
        "task": "app.tasks.some_task",
        "schedule": some_func_retuning_customschedule,  # use a CustomSchedule object
    }
}
"""

# The maximum wait time between each is_due() call on schedulers
# It needs to be higher than the frequency of the schedulers to avoid unnecessary
# is_due() calls
CELERY_BEAT_MAX_LOOP_INTERVAL = 300  # 5 minutes

# Message level tags
MESSAGE_TAGS = {
    messages.DEBUG: "dark",
    messages.ERROR: "danger",
}


# Client settings
API_CLIENT_MAX_TIMEOUT = int(
    get_env_value(
        "API_CLIENT_MAX_TIMEOUT",
        60,
        default_if_blank=True,
    )
)
API_CLIENT_LOG_MAX_AGE_DAYS = int(
    get_env_value(
        "API_CLIENT_LOG_MAX_AGE_DAYS",
        365,
        default_if_blank=True,
    )
)

# social auth
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_REQUIRE_POST = True
SOCIAL_AUTH_USER_FIELDS = ("email", "first_name", "last_name")
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
if GOOGLE_OAUTH_ENABLED:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_env_value(
        "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", None, default_if_blank=True
    )
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_env_value(
        "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", None, default_if_blank=True
    )
