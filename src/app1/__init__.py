default_app_config = 'app1.apps.App1Config'

# IMPORTS
# ------------------------------------------------------------------------------#

from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission


# CUSTOM APP PERMISSIONS
#------------------------------------------------------------------------------#

def add_user_permissions(sender, **kwargs):
    ct = ContentType.objects.get_for_model(model=auth_models.User)
    perm, created = Permission.objects.get_or_create(codename='can_assign_groups', name='Can assign groups',
                                                     content_type=ct)


post_syncdb.connect(add_user_permissions, sender=auth_models)