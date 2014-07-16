# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#

# forms
from django import forms

# http
from django.http import HttpResponseRedirect

# contrib
from django.contrib import admin
# # admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.util import quote
# # auth
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission

# core
from django.core.urlresolvers import reverse

# app1
from app1.models import *

# reversion
import reversion

# Import / Export
from import_export.admin import ImportExportMixin


# OVERRIDES
# ---------------------------------------------------------------------------------------------------------------------#


class ViewList(ChangeList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'View %s' % self.opts.verbose_name_plural.title()

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return reverse('app1:basicmodel_detail', kwargs={'pk': quote(pk)})


class ModelAdminRO(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(ModelAdminRO, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(
            field.name for field in obj._meta.fields
            if not (
                field.name.endswith('_id') or
                field.name == 'id' or
                field.name.endswith('_ptr')
            )
        )
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_changelist(self, request, **kwargs):
        return ViewList

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['read_only'] = True

        return super(ModelAdminRO, self).change_view(
            request, object_id,
            extra_context=extra_context)


# Form overides
class AdvancedModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdvancedModelForm, self).__init__(*args, **kwargs)
        self.fields['fkbasic'].queryset = ChildModel.objects.filter(fkadvanced=self.instance)


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
from import_export import resources

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


@admin.register(AdvancedModel)
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

    #raw_id_fields = ('fkbasic2', 'many2many',)
    # define the related_lookup_fields
    #related_lookup_fields = {
    #    'fk': ['related_fk'],
    #    'm2m': ['related_m2m'],
    #}

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


class ProxyModelAdmin(ModelAdminRO, admin.ModelAdmin):
    list_display_links = None


class ProxyUserAdmin(admin.ModelAdmin):
    pass


class ChildModelAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        """This makes the response after adding go to another apps changelist for some model"""
        return HttpResponseRedirect(reverse('app1:basicmodel_detail', kwargs={'id': str(obj.id)}))


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'codename', 'name']
    list_editable = ['name']





# AUTH MODEL ADMIN OVERRIDE
# ---------------------------------------------------------------------------------------------------------------------#
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('company', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        # Removing the permission part
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        # Keeping the group parts? Ok, but they shouldn't be able to define
        # their own groups, up to you...
        ('Groups', {'fields': ('groups',)}),
        ('Log', {'fields': ('last_login', 'date_joined'), 'classes': ['collapse']}),
    )

    staff_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        # Removing the permission part
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
        #('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        # Keeping the group parts? Ok, but they shouldn't be able to define
        # their own groups, up to you...
        ('Groups', {'fields': ('groups',)}),
        ('Log', {'fields': ('last_login', 'date_joined'), 'classes': ['collapse']}),
    )
    #inlines = [CustomerInline, ]

    filter_horizontal = ('user_permissions', )

    def change_view(self, request, *args, **kwargs):
        # for non-superuser
        if not request.user.is_superuser:
            try:
                self.fieldsets = self.staff_fieldsets
                response = UserAdmin.change_view(self, request, *args, **kwargs)
            finally:
                # Reset fieldsets to its original value
                self.fieldsets = UserAdmin.fieldsets
            return response
        else:
            return UserAdmin.change_view(self, request, *args, **kwargs)

    readonly_fields = ['last_login', 'date_joined']

# ADMIN SITE REGISTERING
# ---------------------------------------------------------------------------------------------------------------------#
# Re-register UserAdmin
#admin.site.unregister(User)
#admin.site.register(User, MyUserAdmin)

admin.site.register(BasicModel, BasicModelAdmin)

admin.site.register(MyUser, MyUserAdmin)

admin.site.register(ChildModel, ChildModelAdmin)
admin.site.register(ProxyModel, ProxyModelAdmin)

admin.site.register(ProxyUser, ProxyUserAdmin)
admin.site.register(Permission, PermissionAdmin)
