#! /bin/sh

exec gunicorn --bind 0.0.0.0:5001 wsgi:app --access-logfile - --timeout 120 --worker-tmp-dir=/dev/shm --workers=1 --threads=1 --worker-class=gthread --log-file=-
