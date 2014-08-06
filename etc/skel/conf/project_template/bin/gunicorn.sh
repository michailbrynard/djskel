#!/bin/bash

BASE_DIR=/home/webapps/Projects/{{ project_name }} 
APP_DIR=$BASE_DIR/app

DJANGO_SETTINGS_MODULE=config.settings.production # which settings file should Django use
DJANGO_WSGI_MODULE=config.wsgi.production # WSGI module name
GUNICORN_CONFIG_FILE=/home/webapps/Projects/{{ project_name }} /etc/gunicorn.conf.py

# Activate the virtual environment
cd $APP_DIR
source /home/webapps/Virtualenvs/{{ project_name }} /bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$APP_DIR:$PYTHONPATH
#export TMPDIR=$BASE_DIR/run
#export TMP=$BASE_DIR/run
#export TEMP=$BASE_DIR/run

exec gunicorn ${DJANGO_WSGI_MODULE}:application --config=${GUNICORN_CONFIG_FILE} --bind=0.0.0.0:8683
