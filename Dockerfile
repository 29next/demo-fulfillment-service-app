FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential curl \
    libpq-dev ffmpeg python3-scipy
#     libmariadbclient-dev \
#     libjpeg62-turbo-dev \
#     zlib1g-dev \
#     libwebp-dev \
#  && rm -rf /var/lib/apt/lists/*

# RUN addgroup --system django \
#     && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy project code
COPY . .

RUN /app/manage.py collectstatic --noinput --clear

# # Run as non-root user
# RUN chown -R django:django /app
# USER django

# Run application
# CMD gunicorn app.wsgi:application
