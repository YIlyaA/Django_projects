from pathlib import Path
from dotenv import load_dotenv
from os import getenv, path
from loguru import logger
from datetime import timedelta

BASE_DIR = (
    Path(__file__).resolve(strict=True).parent.parent.parent
)  # moving three levels up from its location and set it as BASE_DIR

APPS_DIR = BASE_DIR / "core_apps"

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # allow to manage multiple webistes or domains using a single django project
    "django.contrib.humanize",  # provides a set of template filters to help format data a more human readable format
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_spectacular",
    "djoser",
    "cloudinary",
    "django_filters",
    "djcelery_email",
    "django_celery_beat",
]

LOCAL_APPS = [
    "core_apps.user_auth",
    "core_apps.common",
    "core_apps.user_profile",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(APPS_DIR / "templates")
        ],  # set the templates directory into apps directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST"),
        "PORT": getenv("POSTGRES_PORT"),
    }
}


# Argon hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


SITE_ID = 1


STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Loguru setup for advanced logging
LOGGIN_CONFIG = None  # disable the default Django logging configuration

LOGURU_LOGGING = {
    # "handlers": ["console"],   # responsible for dispatching log messages to the appropriate destinations (console output,files email,external services)
    # LOGURU: TRACE(5), DEBUG(10), INFO(20), SUCCESS(25), WARNING(30), ERROR(40), CRITICAL(50)
    "handlers": [
        {
            "sink": BASE_DIR
            / "logs/debug.log",  # This log file will only be responsible for displaying log records with log levels of debug info and warning
            "level": "DEBUG",  # log everything (info, success and warning)
            "filter": lambda record: record["level"].no
            <= logger.level(
                "WARNING"
            ).no,  # log file will include the debug info and warning logs, but exclude error and critical logs
            "format": "{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}",
            "rotation": "10MB",  # when the log file gets to ten megabytes in size, split it and create a new one.
            "retention": "30 days",  # keep the log files for 30 days before deleting them
            "compression": "zip",  # compress the old log files using the zip format
        },
        {
            "sink": BASE_DIR
            / "logs/error.log",  # This log file will only be responsible for displaying log records with log levels of error and critical
            "level": "ERROR",  # log error and critical logs only
            "format": "{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}",
            "rotation": "10MB",
            "retention": "30 days",
            "compression": "zip",
            "backtrace": True,  # include the stack trace of the exception that caused the error
            "diagnose": True,  # include the exception type and message
        },
    ],
}

logger.configure(**LOGURU_LOGGING)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # existing loggers will not be disabled.
    "handlers": {
        "loguru": {
            "class": "interceptor.interceptHandler",
        },
    },
    "root": {
        "handlers": ["loguru"],
        "level": "DEBUG",
    },
}
