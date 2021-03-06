#!/bin/bash

set -ex
cd /usr/src

wait-for-it.sh -t 0 db:5432 -- echo "postgres is up"

admin_password=$ADMIN_PASS || 'admin'

python manage.py migrate
python manage.py loaddata collection.json
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@task3.org', '$admin_password') if not User.objects.filter(username='admin').exists() else 0"

exec "$@"