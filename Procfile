web: uwsgi --chdir=/app --ini=/app/uwsgi.ini

release:  bash -c "python manage.py migrate --no-input && python manage.py collectstatic --no-input"
