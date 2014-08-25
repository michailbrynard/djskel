#!/bin/bash

sudo ln -s {{ project_dir }}/etc/uwsgi/uwsgi_nginx.conf /etc/nging/sites-enabled/
sudo ln -s {{ project_dir }}/etc/uwsgi/uwsgi.ini /etc/uwsgi/vassals/