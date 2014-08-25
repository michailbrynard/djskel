#!/bin/bash

sudo unlink /etc/nginx/sites-enabled/nginx-uwsgi_{{ project_name }}.conf
sudo unlink /etc/uwsgi/uwsgi_{{ project_name }}.ini