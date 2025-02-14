from os import getenv, path       # for production
from dotenv import load_dotenv    # for local testing .env file
from .base import * # noqa
from .base import BASE_DIR


local_env_file = path.join(BASE_DIR, '.envs', ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


SECRET_KEY = getenv('SECRET_KEY')

DEBUG = getenv('DEBUG')

SITE_NAME = getenv('SITE_NAME')

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]   #"0.0.0.0" tels to listen all IPv4 addresses on the local machine

ADMIN_URL = getenv('ADMIN_URL')

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = getenv('EMAIL_PORT')
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL')
DOMAIN = getenv('DOMAIN')

MAX_UPLOAD_SIZE = 1 * 1024 * 1024   # 1MB
