# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# conf.urls
from django.conf.urls import patterns
from django.conf.urls import url

# contrib.auth
from django.contrib.auth.decorators import login_required

# {{ app_name }}
from . import views


# URLS
# ---------------------------------------------------------------------------------------------------------------------#
urlpatterns = patterns('',
    # Static views

    # Generic class based views

    # Custom class based views
    url(r'person/(?P<pk>[0-9]+)/$', login_required(views.PersonView.as_view()),
       name='person_detail'),

    # Custom views
    url(r'/$', '{{ app_name }}.views.about', name='about'),
)