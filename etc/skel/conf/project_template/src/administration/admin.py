# LOGGING
# -----------------------------------------------------------------------------------------------------------------------
import logging

log = logging.getLogger('django')
log.setLevel(logging.INFO)


# IMPORTS
# -----------------------------------------------------------------------------------------------------------------------
# contrib
from django.contrib import admin
from django import forms

from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField

# utils
from django.utils import timezone

# models
from django.contrib.auth.models import User, Group, Permission

from administration.models import MarvalImport
from administration.models import PortalUser, PortalGroup, PortalPermission
from administration.models import Customer, rCustomer, Contact, rContact, Request, rRequest

from read_only.admin import ReadOnlyAdmin


# AUTH MODELADMIN OVERWRITES
# -----------------------------------------------------------------------------------------------------------------------
class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['user_permissions'].required = False

    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text='<a href=\"password/\"><button type="button">Change Password</button></a>'
    )

    class Meta:
        model = User
        #exclude = (
        #    'is_superuser',
        #    'is_staff',
        #)

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'contenttypes']),
        widget=admin.widgets.FilteredSelectMultiple('permissions', is_stacked=False) 
    )


class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'contenttypes']),
        widget=admin.widgets.FilteredSelectMultiple('permissions', is_stacked=False) 
    )
    
class PortalGroupAdmin(GroupAdmin):
    form = GroupEditForm

    
class PortalUserAdmin(UserAdmin):
    form = UserEditForm
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
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
         ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions')}),#, 'is_superuser', 'user_permissions')}),
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


@admin.register(PortalPermission)
class PortalPermissionAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'codename', 'name']
    list_editable = ['name']
  

# re-registering auth models
admin.site.unregister(User)
admin.site.register(PortalUser, PortalUserAdmin)

admin.site.unregister(Group)
admin.site.register(PortalGroup, PortalGroupAdmin)

#from django.contrib.contenttypes.models import ContentType
#admin.site.register(ContentType)
