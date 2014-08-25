# IMPORTS
# ------------------------------------------------------------------------------#

# conf.urls
from django.conf.urls import patterns
from django.conf.urls import url

# contrib.auth
from django.contrib.auth.decorators import login_required

# app1
from skel.app_template import views

urlpatterns = patterns('',
    # Static views
    # url(r'index/$', 'app1.views.index', name='index'),

    # Generic class based views
    url(r'person/(?P<pk>[0-9]+)/$', login_required(views.PersonView.as_view()),
       name='person_detail'),

    # Custom views
    url(r'/$', 'app_name.views.about', name='about'),
)