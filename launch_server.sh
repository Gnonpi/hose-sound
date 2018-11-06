#!/usr/bin/env bash

APP_ENV=$1

echo "Install dependencies"
pipenv sync

echo "Export env vars from .env"
export $(grep -v '^#' config/${APP_ENV}.env | xargs)

echo "Launch Gunicorn server"
pipenv run gunicorn --bind ${SERVICE_HOST}:${SERVICE_PORT} \
    --workers 2 \
    --capture-output --log-level INFO \
    run:application