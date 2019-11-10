#!/usr/bin/env bash

echo "=> Starting database migrations..."
python manage.py makemigrations polls
python manage.py migrate