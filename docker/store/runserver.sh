#!/usr/bin/env sh

echo "Migrations"
python manage.py migrate --noinput

echo "Run manage.py collectstatic"
python manage.py collectstatic --noinput

# invalid length of startup packet error in Postgres
#echo "Create Superuser"
#python manage.py createsuperuser --no-input

echo "Run server"
python manage.py runserver 0.0.0.0:8000

echo "Create Superuser"
python manage.py createsuperuser --no-input

echo "Run celery"
celery -A core worker -l info

echo "Run celery-beat"
celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler