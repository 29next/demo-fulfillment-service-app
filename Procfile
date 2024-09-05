web: gunicorn --pythonpath app app.wsgi:application

release: --pythonpath app django-admin migrate --no-input && django-admin collectstatic --no-input
