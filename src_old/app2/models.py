# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#

# models
from django.db import models

# contrib.auth
from django.contrib.auth.models import User, Group, Permission

from app1.models import BasicModel

# PROXY MODELS
# ---------------------------------------------------------------------------------------------------------------------#

class ProxyModel(BasicModel):
    class Meta:
        proxy = True
        app_label = 'app2'

        permissions = (('view_basicmodel', 'Can view Basic Model'),)
        default_permissions = ()
        verbose_name = "Basic Model"
        verbose_name_plural = "Basic Models"


class ProxyUser(User):
    class Meta:
        proxy = True
        app_label = 'app2'
        verbose_name = User._meta.verbose_name
        verbose_name_plural = User._meta.verbose_name_plural


class ProxyGroup(Group):
    class Meta:
        proxy = True
        app_label = 'app2'
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural


