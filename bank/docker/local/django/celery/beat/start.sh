#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

python manage.py migrate django_celery_beat

em -f './celerybeat.pid'

exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'