#!/bin/bash
sudo mkdir -p /etc/uwsgi/vassals/

sudo ln -s /home/webapps/Projects/djskel/etc/uwsgi/nginx-uwsgi_djskel.conf /etc/nginx/sites-enabled/
sudo ln -s /home/webapps/Projects/djskel/etc/uwsgi/uwsgi_djskel.ini /etc/uwsgi/vassals/

#mkproject djskel
