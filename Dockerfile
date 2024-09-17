FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential curl libpq-dev ffmpeg python3-scipy

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy project code
WORKDIR /app

COPY . .

RUN /app/manage.py collectstatic --noinput --clear

