conda update -y conda

conda env create
source activate {{ project_name }}
pip update pip

cd {{ project_name }}

./bin/initialize.sh
./src/manage.py makemigrations
./src/manage.py migrate
./src/manage.py createsuperuser --username='admin' --email=''

cd ./src/project_pick/static/project_pick

bower install

cd ../../../../

./src/manage.py collectstatic -v0 --noinput