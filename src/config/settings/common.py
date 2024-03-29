"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

__version__ = '0.1'
__author__ = 'JR Minnaar <jr.minnaar@gmail.com>'

ADMINS = (('JR Minnaar', 'jr.minnaar@gmail.com'), )


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------
import logging
logger = logging.getLogger('django')


# DIRECTORIES
# ---------------------------------------------------------------------------------------------------------------------
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.join(os.path.dirname(__file__), '../..')
PROJECT_DIR = os.path.join(BASE_DIR, '../')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ secret_key }}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# APPLICATIONS
# ---------------------------------------------------------------------------------------------------------------------

ADMIN_AUTH = (
    'django.contrib.admin',
    'django.contrib.auth',
)

CONTRIB = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

EXTENSIONS = (
    'filebrowser',
    'grappelli.dashboard',
    'grappelli',
    'import_export',
    'reversion',
    'tinymce',
    'ckeditor',
    'rest_framework',
    'guardian'
)

PROJECT_APPS = (
    # 'basic_demo',
    # 'celerey_demo',
    # 'restful_demo',
    # 'gis_demo',
)

try:
    with open(os.path.join(BASE_DIR, 'config/apps-enabled.txt'), 'r') as f:
        PROJECT_APPS += tuple(f.read().split('\n')[:-1])
except IOError:
    logger.exception('No apps found')

INSTALLED_APPS = CONTRIB + EXTENSIONS + ADMIN_AUTH + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
WSGI_APPLICATION = 'config.wsgi.application'


# Databases
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGES = (
    ('en-za', 'English'),
    ('af', 'Afrikaans'),
)

LANGUAGE_CODE = 'en_ZA'
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

FORMAT_MODULE_PATH = 'config.formats'

# Static files
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'var/www/static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'var/www/media')


# Template files
# ---------------------------------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/howto/static-files/

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)


TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'app/config/templates')]

# LOGGING
# ---------------------------------------------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(PROJECT_DIR, 'var/log/', 'django.log')
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

# LOCAL IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
try:
    from config.settings.extensions.grappelli import *
    from config.settings.extensions.rest_framework import *
    from config.settings.extensions.guardian import *
    from config.settings.extensions.ckeditor import *
except ImportError:
    pass
