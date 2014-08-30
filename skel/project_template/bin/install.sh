#!/bin/bash
sudo mkdir -p /etc/uwsgi/vassals/

ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/nginx-uwsgi_{{ project_name }}.conf /etc/nginx/sites-enabled/
ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/uwsgi_{{ project_name }}.ini /etc/uwsgi/vassals/

mkdir -p var/log
touch var/log/django.log
touch var/log/nginx-error.log
touch var/log/nginc-access.log

./src/manage.py collectstatic
#mkproject {{ project_name }}
