web: python manage.py migrate && python manage.py collectstatic --no-input && gunicorn urlshortener.wsgi:application --workers 1 --threads 2 --timeout 120