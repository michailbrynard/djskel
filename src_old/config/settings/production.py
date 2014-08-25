from config.settings.main import *

DEBUG = True
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ngkdb',
        'USER': 'ngkdb',
        'PASSWORD': 'y6qX85_pmVJhjpo33y-UdDFC',
        'HOST': 'localhost',
        'PORT': '',
    }
}

WSGI_APPLICATION = 'config.wsgi.production.application'

