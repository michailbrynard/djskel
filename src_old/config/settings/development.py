from config.settings.common import *
from config.settings.grappelli import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'src', 'db.sqlite3'),
    }
}


DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'config.wsgi.development.application'

