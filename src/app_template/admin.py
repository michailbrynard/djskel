# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging
logger = logging.getLogger('django')


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# http
#from django.http import HttpResponseRedirect
# contrib
from django.contrib import admin
# # admin
#from django.contrib.admin.views.main import ChangeList
#from django.contrib.admin.util import quote
# # auth
#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User, Permission
# core
#from django.core.urlresolvers import reverse

# reversion
import reversion

# Import / Export
from import_export.admin import ImportExportMixin
from import_export import resources

from read_only.admin import ReadOnlyAdmin

# {{ app_name }}
from .forms import *
from .models import *


# MODEL INLINES
# ---------------------------------------------------------------------------------------------------------------------#
#class AdvancedModelInline(admin.StackedInline):
class AdvancedModelInline(admin.TabularInline):
    model = AdvancedModel  # 1 Foreignkey
    #model = AdvancedModel.many2many.through   # 1 Many2Many
    fk_name = 'fkbasic'  # Multiple Foreignkeys

    fields = ('description', 'fkbasic')

    can_add = True
    can_change = True
    can_delete = False

    verbose_name_plural = 'Plural name here:'
    extra = 2


# RESOURCE CLASSES
# ---------------------------------------------------------------------------------------------------------------------#
class BasicModelResource(resources.ModelResource):

    class Meta:
        model = BasicModel


# MODEL ADMIN
# ---------------------------------------------------------------------------------------------------------------------#
class BasicModelAdmin(ImportExportMixin, reversion.VersionAdmin):
#class BasicModelAdmin(admin.ModelAdmin):
    resource_class = BasicModelResource

    # All fields shortcut
    all = BasicModel._meta.get_all_field_names()

    # Additional fields
    # - by function
    def linkfield(self, obj):
        return '<a href="mailto:%s">%s</a>' % (obj.emailfield, obj.emailfield)

    linkfield.allow_tags = True
    linkfield.short_description = 'Email'
    linkfield.admin_order_field = 'emailfield'

    # - by annotation
    def queryset(self, request):
        from django.db.models import Count

        qs = super(BasicModelAdmin, self).queryset(request)
        return qs.annotate(aggregation=Count('emailfield'))

    def aggregationfield(self, obj):
        return obj.aggregation
    aggregationfield.short_description = 'Aggregation'
    aggregationfield.admin_order_field = 'aggregation'

    # Change|View list options
    list_display = ('charfield', 'integerfield', 'datefield', 'emailfield', 'linkfield')
    list_filter = ['datefield', 'integerfield']
    search_fields = ['charfield']

    # Add|Change form options
    fieldsets = [
        (None, {'fields': ['charfield', 'emailfield', 'htmlfield']}),
        ('Heading1', {'fields': ['datefield', ('decimalfield', 'integerfield')]}),
        ('Heading2', {'fields': ['imagefield', 'urlfield'], 'classes': ['grp-collapse grp-open', ]}),
        #('Admin',    {'fields': ['created_on', 'updated_on' ], 'classes': ['collapse']}),
    ]

    # Inlines
    inlines = [
        AdvancedModelInline,
    ]

    # Admin options
    readonly_fields = ['urlfield']

    #def get_changelist(self, request, **kwargs):
    #    return ViewList


class AdvancedModelAdmin(admin.ModelAdmin):
    # Additional fields
    # - by relation
    @staticmethod
    def fkrelatedfield(obj):
        return obj.fkbasic2.datefield

    fkrelatedfield.short_description = 'datefield'
    fkrelatedfield.admin_order_field = 'fkbasic__datefield'

    # Change|View list options
    list_display = ('description', 'fkbasic', 'created_on')
    list_editable = ['fkbasic', ]

    list_filter = ['fkbasic__integerfield', 'updated_on']
    date_hierarchy = 'updated_on'
    search_fields = ['description', 'fkbasic__charfield']

    # Add|Change form options
    fieldsets = [
        #(None, {'fields': ['description', 'fkbasic', 'fkbasic2']}),
        (None, {'fields': ['description', 'fkbasic']}),
        ('Relations', {'fields': ['many2many'], 'classes': ['wide']}),
        ('Quality', {'fields': [('created_on', 'updated_on'), 'note'], 'classes': ['collapse']}),
    ]
    filter_horizontal = ('many2many',)

    # Admin options
    readonly_fields = ['created_on', 'updated_on']

    raw_id_fields = ('fkbasic',)
    autocomplete_lookup_fields = {
        'fk': ['fkbasic'],
    }

    # Overrides
    form = AdvancedModelForm

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.description = 'Newly created!'
        obj.description = obj.description + 'Just updated!'
        obj.save()


class PersonAdmin(admin.ModelAdmin):
    all = Person._meta.get_all_field_names()
    list_display = [field for field in all if not (field.endswith('_id') or field == 'id' or field.endswith('_ptr'))]

class CompanyAdmin(admin.ModelAdmin):

    # - by annotation
    def queryset(self, request):
        from django.db.models import Count

        qs = super(CompanyAdmin, self).queryset(request)
        return qs.annotate(aggregation=Count('person'))

    @staticmethod
    def aggregationfield(obj):
        return obj.aggregation
    aggregationfield.short_description = 'Employees'
    aggregationfield.admin_order_field = 'aggregation'

    # Change|View list options
    list_display = ('name', 'owner', 'aggregationfield')
    search_fields = ['name', 'owner__name']


admin.site.register(Person, PersonAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(AdvancedModel, AdvancedModelAdmin)
admin.site.register(BasicModel, BasicModelAdmin)