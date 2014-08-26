#!/bin/bash
mkdir -p /etc/uwsgi/vassals/

ln -s /home/webapps/Projects/djskel/etc/uwsgi/nginx-uwsgi_djskel.conf /etc/nginx/sites-enabled/
ln -s /home/webapps/Projects/djskel/etc/uwsgi/uwsgi_djskel.ini /etc/uwsgi/vassals/

mkdir -p var/log
touch var/log/django.log
touch var/log/nginx-error.log
touch var/log/nginc-access.log

#mkproject djskel
