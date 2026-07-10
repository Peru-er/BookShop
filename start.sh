
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:8000
python manage.py createsuperuser_if_none
