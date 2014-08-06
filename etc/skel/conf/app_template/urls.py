# IMPORTS
# ------------------------------------------------------------------------------#

# conf.urls
from django.conf.urls import patterns
from django.conf.urls import url

# contrib.auth
from django.contrib.auth.decorators import login_required

# app1
from app1 import views

urlpatterns = patterns('',
    # Static views
    # url(r'index/$', 'app1.views.index', name='index'),

    # Generic views
    url(r'basicmodel/(?P<pk>[0-9]+)/$', login_required(views.BasicModelView.as_view()),
       name='basicmodel_detail'),

    # Custom views
    url(r'basicmodel/save/$', 'app1.views.custom_basic_save_view', name='basicmodel_save'),
)