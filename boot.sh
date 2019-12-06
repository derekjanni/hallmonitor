#! /bin/sh
sqlite3 hallmonitor.db -c "create table if not exists create table endpoint(name varchar(20), endpoint_id int, result smallint, status_code smallint, time float);"
exec gunicorn --bind 0.0.0.0:5001 wsgi:app --access-logfile - --timeout 120 --worker-tmp-dir=/dev/shm --workers=1 --threads=1 --worker-class=gthread --log-file=-
