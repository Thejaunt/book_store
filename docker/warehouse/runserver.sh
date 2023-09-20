#!/usr/bin/env sh

echo "Migrations"
python manage.py migrate --noinput

echo "Run manage.py collectstatic"
python manage.py collectstatic --noinput

echo "Run server"
python manage.py runserver 0.0.0.0:8002

