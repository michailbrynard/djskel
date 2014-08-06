# IMPORTS
#-----------------------------------------------------------------------------------------------------------------------#
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList


# OVERWRITES
#-----------------------------------------------------------------------------------------------------------------------#
class ViewList(ChangeList):
    def __init__(self, *args, **kwargs):
        super(ViewList, self).__init__(*args, **kwargs)
        self.title = 'View %s' % self.opts.verbose_name_plural.title()
    
class ReadOnlyAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(ReadOnlyAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(field.name for field in 
         obj._meta.fields if not 
             (field.name.endswith('_id') or field.name =='id' or field.name.endswith('_ptr')))
        return readonly_fields
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_changelist(self, request, **kwargs):
        return ViewList
    
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['read_only'] = True

        return super(ReadOnlyAdmin, self).change_view(request, object_id, extra_context=extra_context)
