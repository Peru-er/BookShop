
python manage.py migrate
gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:8000
