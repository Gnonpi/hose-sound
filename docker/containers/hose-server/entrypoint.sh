cd /opt/hose-sound

export APP_ENV=dev
poetry run python hose/manage.py makemigrations
poetry run python hose/manage.py migrate