web: gunicorn --pythonpath app app.wsgi:application

release: sh -c 'cd app && python manage.py migrate --no-input && python manage.py collectstatic --no-input'
