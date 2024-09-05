web: gunicorn --pythonpath app app.wsgi:application

release: django-admin migrate --no-input && django-admin collectstatic --no-input
