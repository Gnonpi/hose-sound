cd /opt/hose-sound

set -e

# Wait db container to be up
sleep 2

echo "> Making migrations"
APP_ENV=dev poetry run python hose/manage.py makemigrations
echo "> Running migrations"
APP_ENV=dev poetry run python hose/manage.py migrate
echo "> Running with gunicorn"
APP_ENV=dev poetry run gunicorn hose.wsgi