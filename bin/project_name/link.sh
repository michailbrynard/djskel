#!/bin/bash
sudo chown -R canary:webapps /home/webapps/Projects/{{ project_name }}
sudo chmod -R g+w /home/webapps/Projects/{{ project_name }}

ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/nginx-uwsgi_{{ project_name }}.conf /etc/nginx/sites-enabled/
ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/uwsgi_{{ project_name }}.ini /etc/uwsgi/vassals/

sudo service nginx restart