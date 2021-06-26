#!/bin/sh

chmod u+x migration.sh

if [ "$1" == first ]; then
  python manage.py db init
  python manage.py db migrate
  python manage.py db upgrade
else
  python manage.py db migrate
  python manage.py db upgrade
fi