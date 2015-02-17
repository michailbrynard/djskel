DJSKEL - Django Project template
================================

DjSkel is a heavyweight project template for Django. The folder structure is set up to mimic UNIX folder structure. The django source directory is src.

How to use
----------
1. Download and install [Anaconda](https://warehouse.python.org/project/gunicorn/) for Python 3.4
2. Create virtual python environment
    ```bash
    export PATH=~/anaconda3/bin/:$PATH
    conda update conda
    conda create -n webdev python=3.4 pip django
    source activate webdev
    ```

3. Create django project from template
```bash
django-admin startproject --template=https://github.com/obitec/djskel/archive/master.zip --extension=py --extension=conf --extension=sh --extension=ini {{ project_name }}
```
4. Run the installer
```bash
```


How to deploy
-------------
1. 




Feutures
--------
- Django 1.7 or newer
- UWSGI
- Gunicorn
- Nginx
- Postgresql
- Fig
- Docker
- Vagrant
- Celery (TODO)
- Redis (TODO)
- Custom User model (TODO)
- Munin
- 

Django Extensions
-----------------
- Grappelli
- Rest Framework 3
- Guardian
- Report Builder

Custom Apps
--------------
- Munin
- FactBook
- Issue Tracker


