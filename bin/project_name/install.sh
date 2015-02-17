#!/bin/bash

ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/nginx-uwsgi_{{ project_name }}.conf /etc/nginx/sites-enabled/
ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/uwsgi_{{ project_name }}.ini /etc/uwsgi/vassals/

mkdir -p var/log
mkdir -p var/www/media/uploads
mkdir -p tmp

touch var/log/django.log
touch var/log/nginx-error.log
touch var/log/nginx-access.log

touch tmp/uwsgi.sock

./src/manage.py collectstatic -v0 --noinput
#mkproject {{ project_name }}

sudo touch /etc/uwsgi/emporer.ini
sudo chown canary:webapps /etc/uwsgi/emperor.ini

cat <<EOT >> /etc/uwsgi/emperor.ini
[uwsgi]
emperor         = /etc/uwsgi/vassals
master          = true
uid             = webapps
gid             = webapps
daemonize       = /home/webapps/emporer.log
pidfile         = /home/webapps/emporer.pid
vacuum          = true
EOT

#uwsgi -c /etc/uwsgi/emperor.ini 

cd var/www/static/app/
bower install
cd /home/webapps/Projects/{{ project_name }}

sudo chown -R canary:webapps /home/webapps/Projects/{{ project_name }}
sudo chmod -R g+w /home/webapps/Projects/{{ project_name }}

./bin/emporer/reload.sh

