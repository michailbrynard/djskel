default_app_config = '{{ app_name }}.apps.CustomConfig'

#from django.db.models.signals import post_syncdb
#from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth import models


# custom user related permissions
#def add_user_permissions(sender, **kwargs):
#    ct = ContentType.objects.get_for_model(model=models.User)
#    perm, created = models.Permission.objects.get_or_create(codename='can_use_{{ app_name }}', name='Can use {{ app_name }}', content_type=ct)#

#post_syncdb.connect(add_user_permissions, sender=models)