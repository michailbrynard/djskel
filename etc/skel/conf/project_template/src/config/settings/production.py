from config.settings.common import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'config.wsgi.production.application'
BASE_URL = 'http://127.0.0.1/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': os.path.join(BASE_DIR, 'django.db'),
    },
}