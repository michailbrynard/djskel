#!/bin/bash
sudo mkdir -P /etc/uwsgi/vassals/

sudo ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/nginx-uwsgi_{{ project_name }}.conf /etc/nging/sites-enabled/
sudo ln -s /home/webapps/Projects/{{ project_name }}/etc/uwsgi/uwsgi_{{ project_name }}.ini /etc/uwsgi/vassals/

#mkproject {{ project_name }}
