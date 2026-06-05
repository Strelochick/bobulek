#!/bin/sh
set -e

if [ "${USE_POSTGRES}" = "True" ]; then
  until nc -z "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}"; do
    echo "Waiting for PostgreSQL..."
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ]; then
  python manage.py createsuperuser --noinput || true
fi

exec "$@"
