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
from app2.models import ProxyModel, ProxyUser, ProxyGroup

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



class ProxyModelAdmin(ModelAdminRO, admin.ModelAdmin):
    list_display_links = None


class ProxyUserAdmin(admin.ModelAdmin):
    pass


# ADMIN SITE REGISTERING
# ---------------------------------------------------------------------------------------------------------------------#

admin.site.register(ProxyModel, ProxyModelAdmin)

admin.site.register(ProxyUser, ProxyUserAdmin)
admin.site.register(Permission, PermissionAdmin)

