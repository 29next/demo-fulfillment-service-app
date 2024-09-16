FROM calltracker/calltracker-python-base:latest


ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


WORKDIR /app

# RUN addgroup --system django \
#     && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy project code
COPY . .

RUN python manage.py collectstatic --noinput --clear

# # Run as non-root user
# RUN chown -R django:django /app
# USER django

# Run application
CMD gunicorn app.wsgi:application
