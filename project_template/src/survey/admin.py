# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
from django.contrib import admin
# from django.contrib.admin.views.main import ChangeList
# from django.contrib.admin.util import quote
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User, Permission
# from django.core.urlresolvers import reverse
from guardian.admin import GuardedModelAdmin
import reversion
# from import_export.admin import ImportExportMixin
# from import_export import resources
# from read_only.admin import ReadOnlyAdmin
from django import forms
from .models import *
from django.forms import CheckboxSelectMultiple
from logging import getLogger
from survey.forms import ChallengeDetailForm
from import_export import resources
from import_export import fields
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV, XLS, HTML


# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
logger = getLogger('django')


# Resources
# ---------------------------------------------------------------------------------------------------------------------#
class SurveyResource(resources.ModelResource):
    # published = fields.Field(column_name='published_date')
    class Meta:
        model = Survey

        # genders = fields.Field()
        # country = fields.Field(column_name='country_of_operation__name')

        fields = (
            # Basic
            'id', 'slug', 'name', 'gender', 'company_name', 'job_title', 'country_of_operation__name',
            'email_address', 'phone_number',
            # Company
            'country_or_region', 'countries', 'vas_parties', 'service_pitches'
            # Financial
            'investments', 'currency',
            'revenue_mar_14', 'revenue_jun_14', 'revenue_sep_14', 'revenue_dec_14',
            'revenue_stream_1__name', 'revenue_stream_2__name', 'revenue_stream_3__name', 'vas_revenue_share',
            'acceptable_roi_wait', 'acceptable_roi_percentage',
            # Challenges
            'challenges',
        )

        # def dehydrate_genders(self):
        #     return '%s' % (self.model.get_gender_display())


class VASProviderResource(resources.ModelResource):
    class Meta:
        model = VASProvider


class ChallengeDetailResource(resources.ModelResource):
    class Meta:
        model = ChallengeDetail


# MODEL FORMS
# ---------------------------------------------------------------------------------------------------------------------#
class SurveyAdminForm(forms.ModelForm):
    class Meta:
        model = Survey
        widgets = {
            'challenges': CheckboxSelectMultiple(),
        }


class VASProviderAdminForm(forms.ModelForm):
    class Meta:
        model = VASProvider


class ChallengeDetailAdminForm(forms.ModelForm):
    class Meta:
        model = ChallengeDetail


# MODEL ADMIN
# ---------------------------------------------------------------------------------------------------------------------#
class VASProviderAdmin(ImportExportModelAdmin):
    resource_class = VASProviderResource
    formats = (CSV, XLS, HTML)
    change_list_template = 'admin/import_export/change_list_export.html'
    form = VASProviderAdminForm

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


class VASProviderInline(admin.StackedInline):
    form = VASProviderAdminForm

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    model = VASProvider  # 1 Foreignkey

    can_add = True
    can_change = True
    can_delete = True

    # verbose_name_plural = 'Plural name here:'
    extra = 0


class ChallengeDetailAdmin(ImportExportModelAdmin):
    resource_class = ChallengeDetailResource
    formats = (CSV, XLS, HTML)
    change_list_template = 'admin/import_export/change_list_export.html'

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    list_display = ['challenge', 'respondent']


class ChallengeDetailInline(admin.StackedInline):
    form = ChallengeDetailAdminForm

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    model = ChallengeDetail  # 1 Foreignkey

    can_add = False
    can_change = True
    can_delete = False

    # verbose_name_plural = 'Plural name here:'
    extra = 0


class SurveyAdmin(ImportExportModelAdmin, GuardedModelAdmin):
    form = SurveyAdminForm
    resource_class = SurveyResource
    formats = (CSV, XLS, HTML)
    change_list_template = 'admin/import_export/change_list_export.html'
    # change_list_template = "admin/change_list_filter_sidebar.html"

    # Change|View list options
    list_display = ('name', 'company_name', 'email_address', 'country_of_operation', 'survey_link')
    list_filter = ['country_of_operation', 'gender']
    search_fields = ['name', 'company_name', 'email_address']

    fieldsets = [
        ('Survey Overview', {
            'fields': ['is_section_0_reviewed',
                       'is_section_1_reviewed',
                       'is_section_2_reviewed',
                       'is_section_3_reviewed', ],
            'classes': ['grp-collapse grp-closed']}),
        ('Basic Information', {
            'fields': ['slug', 'name', 'gender', 'company_name', 'job_title',
                       'country_of_operation', 'email_address', 'phone_number', ]}),
        ('Company Role', {
            'fields': ['country_or_region', 'countries', 'vas_parties', 'service_pitches'],
            'classes': ['grp-collapse grp-closed', ]}),
        ('VAS Providers', {
            'fields': (),
            'classes': ["placeholder vasprovider_set-group grp-collapse grp-closed"]}),
        ('Financial', {
            'fields': ['investments', 'currency',
                       'revenue_mar_14', 'revenue_jun_14', 'revenue_sep_14', 'revenue_dec_14',
                       'revenue_stream_1', 'revenue_stream_2', 'revenue_stream_3', 'vas_revenue_share',
                       'acceptable_roi_wait', 'acceptable_roi_percentage', ],
            'classes': ['grp-collapse grp-closed']}),
        ('Challenges', {
            'fields': ['challenges', ],
            'classes': ['grp-collapse grp-closed']}),
        ('Challenge Details', {
            'fields': (),
            'classes': ["placeholder challengedetail_set-group"]}),
    ]

    def survey_link(self, obj):
        from django.contrib.sites.models import Site

        current_site = Site.objects.get_current()
        return '<a href="http://{0}">http://{0}</a>'.format(
            current_site.domain + reverse('survey:login', kwargs={'slug': obj.slug}))

    survey_link.allow_tags = True
    survey_link.short_description = "View"

    inlines = [
        VASProviderInline,
        ChallengeDetailInline,
    ]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'private', 'owner']
    list_filter = ['private', ]
    search_fields = ['name', ]


class ReliableAdmin(admin.ModelAdmin):
    list_display = ['name', 'private', 'owner']
    list_filter = ['private', ]
    search_fields = ['name', ]


class PeriodAdmin(admin.ModelAdmin):
    list_display = ['name', 'private', 'owner']
    list_filter = ['private', ]
    search_fields = ['name', ]


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['name', 'private', 'owner']
    list_filter = ['private', ]
    search_fields = ['name', ]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Reliable, ReliableAdmin)
admin.site.register(Period, PeriodAdmin)

admin.site.register(ChallengeDetail, ChallengeDetailAdmin)
admin.site.register(VASProvider, VASProviderAdmin)