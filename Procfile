web: uwsgi --chdir=/app --ini=/app/uwsgi.ini

worker: celery -A app worker -l info -Q celery --without-heartbeat

beat: celery -A app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

release:  bash -c "python manage.py migrate --no-input && python manage.py collectstatic --no-input"
