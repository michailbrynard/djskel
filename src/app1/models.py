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

# core
from django.core.urlresolvers import reverse

# utils
from django.utils import timezone

# tinymce
from tinymce.models import HTMLField

# MIXIN MODELS
# ---------------------------------------------------------------------------------------------------------------------#


class MixinModel(models.Model):
    # Quality fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)

    class Meta:
        abstract = True


class AbstractBaseModel(models.Model):
    # Quality fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    note = models.TextField(blank=True)

    class Meta:
        abstract = True


# BASE MODELS
# ---------------------------------------------------------------------------------------------------------------------#

class BasicModel(models.Model):
    #id          = models.AutoField(primary=True)
    slug = models.SlugField(max_length=50)

    charfield = models.CharField(max_length=50, blank=True)
    integerfield = models.IntegerField()
    booleanfield = models.BooleanField(default=False)
    htmlfield = HTMLField()

    OPTION1 = 'O1'
    OPTION2 = 'O2'

    CHOICES = (
        (OPTION1, 'Option One'),
        (OPTION2, 'Option Two'),
    )
    choicefield = models.CharField(
        max_length=3,
        choices=CHOICES,
        default=OPTION1
    )

    decimalfield = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    datefield = models.DateField(null=True, blank=True)
    emailfield = models.EmailField(blank=True)
    urlfield = models.URLField(blank=True, null=True)
    imagefield = models.ImageField(upload_to='images', null=True, blank=True)

    #Grappelli
    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "charfield__icontains",)

    # Methods
    def model_method(self):
        if self.choicefield:
            return "%s %s" % (self.get_choicefield_display(), self.charfield)
        else:
            return "%s" % (self.charfield)

    model_method.admin_order_field = 'charfield'
    model_method.short_description = 'If then display'

    # Overrides
    def get_absolute_url(self):
        return reverse('app1:basicmodel_detail', kwargs={'slug': self.slug})

    def __str__(self):  #Python 3
        return "%s" % (self.charfield.title())

    class Meta:
        managed = True

        app_label = 'app1'

        verbose_name = "Basic Model"
        verbose_name_plural = "Basic Models"
        ordering = ['charfield']
        get_latest_by = "order_date"

        permissions = (('permission_code', 'Human readable permission name'),)
        default_permissions = ('add', 'change', 'delete')

        unique_together = (('emailfield', 'charfield'),)


# MODELS
# ---------------------------------------------------------------------------------------------------------------------#

class AdvancedModel(MixinModel, models.Model):
    description = models.CharField(max_length=45, blank=False)
    fkbasic = models.ForeignKey(BasicModel, null=True, blank=True, verbose_name='Basic Foreignkey Filtered')
    #fkbasic2 = models.ForeignKey(BasicModel, related_name='basic_other', verbose_name='Basic Foreignkey')

    many2many = models.ManyToManyField(BasicModel, related_name='related_many', verbose_name='Many 2 Many Relation')

    def __str__(self):
        return self.description


# EXTEND MODELS
# ---------------------------------------------------------------------------------------------------------------------#

class ChildModel(BasicModel):
    fkadvanced = models.ForeignKey(AdvancedModel)
    additionalfield = models.CharField(max_length=45, blank=False)


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


class MyUser(User):
    company = models.CharField(max_length=50)
        

