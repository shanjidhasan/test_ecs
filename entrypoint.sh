#!/bin/sh
# entrypoint.sh: Run migrations and then start Gunicorn

python manage.py migrate --settings=testproject.settings_ecs
exec gunicorn testproject.wsgi:application --bind 0.0.0.0:8000
