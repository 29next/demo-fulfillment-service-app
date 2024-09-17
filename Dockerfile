FROM ubuntu:20.04

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


# Install Python and dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python-is-python3 libpq-dev

# Install system packages required by Wagtail and Django.
# RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
#     build-essential curl \
#     libpq-dev ffmpeg
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
CMD gunicorn app.wsgi:application
