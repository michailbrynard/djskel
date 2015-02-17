#!/bin/bash

unlink /etc/nginx/sites-enabled/nginx-uwsgi_{{ project_name }}.conf
unlink /etc/uwsgi/vassals/uwsgi_{{ project_name }}.ini

service nginx restart
