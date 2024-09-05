web: gunicorn --pythonpath app app.wsgi:application

release: sh -c 'cd app && python manage.py migrate && python manage.py collectstatic'
