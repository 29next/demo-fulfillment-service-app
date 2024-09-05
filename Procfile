web: gunicorn --pythonpath app app.wsgi:application

release: cd app && django-admin migrate --no-input && django-admin collectstatic --no-input
