import os
import multiprocessing

APP_NAME = 'ngkdb'
BASE_DIR = os.path.join('/home/webapps/Projects/', APP_NAME)
proc_name = APP_NAME
user = APP_NAME 
group = 'webapps'
workers = multiprocessing.cpu_count() * 2 + 1
log_level = 'debug'
#bind = 'unix:%s' % os.path.join(BASE_DIR, 'run/gunicorn.sock')
timeout = 30
max_requests = 200
daemon = False
#pidfile = os.path.join(BASE_DIR, 'run/gunicorn.pid')
#umask = 0o011
#tmp_upload_dir = os.path.join(BASE_DIR, 'run/tmp/')
#worker_tmp_dir = os.path.join(BASE_DIR, 'run/tmp/') 
#raw_env = ['TMPDIR=%s' % os.path.join(BASE_DIR, 'run/tmp/')]#,'DJANGO_SETTINGS_MODULE=config.settings.production']
