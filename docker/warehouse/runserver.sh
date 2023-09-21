#!/usr/bin/env sh

echo "Migrations"
python manage.py migrate --noinput

echo "Run manage.py collectstatic"
python manage.py collectstatic --noinput

echo "Create Superuser"
python manage.py createsuperuser --no-input

echo "Run server"
python manage.py runserver 0.0.0.0:8002

# i don't know why. it just worked
echo "Create Superuser"
python manage.py createsuperuser --no-input