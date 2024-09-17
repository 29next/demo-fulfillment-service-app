web: which uwsgi && uwsgi --chdir=/app --ini=/app/uwsgi.ini

release: python manage.py migrate --no-input && ptyon manage.py collectstatic --no-input
