#!/bin/bash

django-admin startproject --template=skel/project_template --extension=py --extension=conf --extension=sh --extension=ini djskel

mv djskel/* ./
mv djskel/.gitignore ./
rm -R djskel

chmod +x src/manage.py

pip install -U -r var/requirements/development.txt

./src/manage.py syncdb

./src/manage.py startapp --template=skel/app_template --extension=py demo_app
mv demo_app src/
echo demo_app >> src/config/apps-enabled.txt

./src/manage.py makemigrations demo_app
./src/manage.py migrate demo_app

./src/manage.py createsuperuser

mkdir var/log
touch var/log/django.log
touch var/log/nginx-error.log
touch var/log/nginc-access.log

# Run after spwaning uwsgi emperor
chown canary:webapps tmp/uwsgi.sock

./src/manage.py runserver

