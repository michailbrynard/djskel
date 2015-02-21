# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from survey.views import ProviderCreate, ProviderDelete, ProviderUpdate, ChallengeDetailUpdate, ChallengeDetailCreate


# URLS
# ---------------------------------------------------------------------------------------------------------------------#
urlpatterns = patterns(
    '',  # namespace

    url(r'^s/(?P<slug>\w{12,})/$', 'survey.views.login_user', name='login'),
    url(r'^welcome/$', 'survey.views.about', name='about'),
    url(r'^goodbye/$', TemplateView.as_view(template_name='survey/goodbye.html'), name='goodbye'),

    url(r'^$', 'survey.views.survey', name='survey'),

    url(r'^profile/$', 'survey.views.update_profile', name='update_profile'),
    url(r'^providers/$', 'survey.views.update_providers', name='update_providers'),
    url(r'^financial/$', 'survey.views.update_financial', name='update_financial'),
    url(r'^challenge/$', 'survey.views.update_challenge', name='update_challenge'),

    # url(r'^(?P<slug>\w{4,})/vas/(?P<vas_id>\d{1,3})', 'survey.views.update_provider', name='update_provider'),
    # url(r'^vas/$', 'survey.views.provider', name='provider'),

    # API Stuff
    # url(r'^provider/add/$', 'survey.views.create_provider', name='create_provider'),
    # url(r'^provider/update/(?P<pk>\d+)$', 'survey.views.update_provider', name='update_provider'),
    # url(r'^provider/delete/$', 'survey.views.delete_provider', name='delete_provider'),

    # url(r'^challenge_detail/$', 'survey.views.update_challenge_detail', name='update_challenge_detail'),
    # url(r'^playground/$', TemplateView.as_view(template_name='survey/index.html'), name='playground'),

    url(r'^service/add/$', 'survey.views.add_service', name='add_service'),
    url(r'^challenge/add/$', 'survey.views.add_challenge', name='add_challenge'),
    url(r'^challenge/reorder/$', 'survey.views.reorder_challenge', name='reorder_challenge'),
    url(r'^reliable/add/$', 'survey.views.add_reliable', name='add_reliable'),
    url(r'^period/add/$', 'survey.views.add_period', name='add_period'),

    url(r'^review/$', 'survey.views.update_section_status', name='update_section_status'),

    url(r'^provider/add/$', ProviderCreate.as_view(), name='provider_add'),
    url(r'^provider/(?P<pk>\d+)/$', ProviderUpdate.as_view(), name='provider_update'),
    url(r'^provider/(?P<pk>\d+)/delete/$', ProviderDelete.as_view(), name='provider_delete'),

    url(r'^challenge_detail/(?P<rank>\d+)/$', ChallengeDetailUpdate.as_view(), name='challenge_detail_update'),
    url(r'^challenge_detail/add/$', ChallengeDetailCreate.as_view(), name='challenge_detail_add'),

)
