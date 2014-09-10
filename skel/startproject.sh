#!/bin/bash

#mkproject djskel
mkproject {{ project_name }}

#django-admin startproject --template=skel/project_template --extension=py --extension=conf --extension=sh --extension=ini djskel
django-admin startproject --template=skel/project_template --extension=py --extension=conf --extension=sh --extension=ini {{ project_name }}

#mv djskel/* ./
#mv djskel/.gitignore ./
#rm -R djskel
mv {{ project_name }}/* ./
mv {{ project_name }}/.gitignore ./
rm -R {{ project_name }}

chmod +x src/manage.py

pip install -U -r var/requirements/development.txt

mkdir -p tmp
mkdir -p var/log
touch src/config/apps-enabled.txt
touch var/log/django.log
touch var/log/nginx-error.log
touch var/log/nginc-access.log

./src/manage.py syncdb


#./src/manage.py startapp --template=skel/app_template --extension=py demo_app
#mv demo_app src/
#echo demo_app >> src/config/apps-enabled.txt

./src/manage.py startapp --template=skel/app_template --extension=py {{ app_name }}
mv {{ app_name }} src/
echo {{ app_name }} >> src/config/apps-enabled.txt
./src/manage.py makemigrations {{ app_name }}
./src/manage.py migrate {{ app_name }} 

./src/manage.py createsuperuser

# Run after spwaning uwsgi emperor
chown canary:webapps tmp/uwsgi.sock

./src/manage.py runserver


git add -A
git commit -a -m "Skeleton app added from djskel"
git push --set-upstream origin master
