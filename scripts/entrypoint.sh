#!/bin/sh

# Exit sctipt if any errors.
set -e
# Proxy can serve static files really efficiently.
# Allow us to collect all static in one location.
python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

# Starts the django project.
uwsgi --socket :8000 --master --enable-threads --module WhatArePeopleSayingAbout.wsgi