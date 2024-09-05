web: gunicorn --pythonpath app app.wsgi:application

release: -sh -c 'cd app && django-admin migrate --no-input && django-admin collectstatic --no-input'
