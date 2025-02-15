#!/bin/bash

# exit if a command exits with a non-zero status
set -o errexit

# exit if pipline failed
set -o pipfail

# exit if an uninitialized variable is used
set -o nounset

python manage.py migrate --no-input
python manage.py collectstatic --no-input
exec python manage.py runserver 0.0.0.0:8000