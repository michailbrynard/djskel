from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

from filebrowser.sites import site

from django.contrib import admin
from django.contrib.auth.views import login


urlpatterns = patterns('',
    # Examples:
    (r'^$', RedirectView.as_view(url='/admin/')),
    
    # Login
    #(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    
    # App Url
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    (r'^tinymce/', include('tinymce.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('restful_api.urls',  namespace='restful')),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)