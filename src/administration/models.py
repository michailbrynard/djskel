# LOGGING
# ---------------------------------------------------------------------------------------------------------------------#
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# IMPORTS
# ---------------------------------------------------------------------------------------------------------------------#
# django
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.urlresolvers import reverse

# time
from django.utils import timezone
import calendar
import time

# random slug
import os
import binascii


def get_random_slug(tz):
    return hex(int(str(tz)[:7]))[5:] + binascii.b2a_hex(os.urandom(5)).decode()


# MANAGERS
# ---------------------------------------------------------------------------------------------------------------------#
class CustomerManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


# MODELS
# ---------------------------------------------------------------------------------------------------------------------#
class Period(models.Model):
    year = models.IntegerField()

    MONTH_CHOICES = tuple((i + 1, m) for i, m in enumerate(calendar.month_name[1:]))
    month = models.IntegerField(choices=MONTH_CHOICES)

    def datetime_start(self):
        return timezone.datetime(self.year, self.month, 1)

    def datetime_end(self):
        return timezone.datetime(self.year, self.month,
                                 calendar.monthrange(self.year, self.month)[1], 23, 59, 59)

    def display_start(self):
        return self.datetime_start().strftime('%Y-%m-%d')

    def display_end(self):
        return self.datetime_end().strftime('%Y-%m-%d')

    def jsontime_start(self):
        return int(time.mktime(self.datetime_start().timetuple()))

    def jsontime_end(self):
        return int(time.mktime(self.datetime_end().timetuple()))+1

    def short_format(self):
        self.datetime_start().strftime('%b\u00a0%y')

    def __str__(self):
        return self.datetime_start().strftime('%B %Y')

    class Meta:
        default_permissions = ()


class Customer(models.Model):
    code = models.CharField(max_length=6, unique=True)

    def natural_key(self):
        return self.code

    name = models.CharField(max_length=100, blank=True)

    objects = CustomerManager()

    def option(self):
        return '<option value="%s">%s - %s</option>' % (
            reverse('app_name:url_customer', args=[self.code]), self.code, self.name)

    BASIC = 'basic'
    ADVANCED = 'advanced'
    LEVEL_CHOICES = (
        (BASIC, 'Basic'),
        (ADVANCED, 'Advanced'),
    )
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default=BASIC)
    sla = models.DecimalField(decimal_places=2, max_digits=4, default=89.00)
    groupname = models.CharField(max_length=30, blank=True)

    # users = models.ManyToManyField(User, null=True, blank=True,
    # related_name='customer_users', verbose_name='Authorized Users')

    #contacts = models.ManyToManyField(
    # User, null=True, blank=True,
    # through='Contact',
    # related_name='customer_contact', verbose_name='Contacts')

    slug = models.SlugField(max_length=13, editable=False)
    auto = models.BooleanField(default=False, editable=True)

    #def get_absolute_url(self):
    #    return reverse('reporting:customer_detail', kwargs={'slug':str(self.slug)})

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = get_random_slug(timezone.now().timestamp())
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.code, self.name)

    class Meta:
        ordering = ['code']
        #app_label = 'administration'
        #verbose_name = 'EOH Customer'
        #verbose_name_plural = 'EOH Customers'


class rCustomer(Customer):
    class Meta:
        proxy = True
        # app_label = 'administration'

        default_permissions = ()
        permissions = (
            ('change_rcustomer', 'Can view customer only'),
        )

        verbose_name = Customer._meta.verbose_name
        verbose_name_plural = Customer._meta.verbose_name_plural


class Contact(models.Model):
    user = models.ForeignKey(User)
    # Alternatively, limit to single group, thought not so maintainable as there is more than one group
    # user = models.ForeignKey(User, limit_choices_to={'groups__name': 'SLA Report Customer'})
    customer = models.ForeignKey(Customer)

    IRIS_ROLE_CHOICES = (
        ('IRIS-CUSTOMER', 'Customer'),
        ('IRIS-USER', 'User'),
    )

    IRIS_SSO_TYPE = (
        ('groupname', 'Customer Group'),
        ('code', 'Customer'),
    )

    iris_role = models.CharField(max_length=14, choices=IRIS_ROLE_CHOICES, default='IRIS-CUSTOMER')
    iris_sso_type = models.CharField(max_length=10, choices=IRIS_SSO_TYPE, default='code')

    def customer_description(self):
        return self.customer.__str__()

    customer_description.admin_order_field = 'customer__code'

    def user_name(self):
        return self.user.username + ' (' + self.user.get_short_name() + ')'

    user_name.admin_order_field = 'user__username'

    class Meta:
        pass
        #app_label = 'administration'


class rContact(Contact):
    class Meta:
        proxy = True
        # app_label = 'administration'

        default_permissions = ()
        permissions = (
            ('change_rcontact', 'Can view contact only'),
        )
        verbose_name = Contact._meta.verbose_name
        verbose_name_plural = Contact._meta.verbose_name_plural


class Request(models.Model):
    call_ref = models.PositiveIntegerField(unique=True, verbose_name='Req Number')

    contact = models.CharField(max_length=64, blank=True)
    customer = models.ForeignKey(Customer)

    created_on = models.DateTimeField(blank=True, null=True, verbose_name='Date and time logged')
    solved_on = models.DateTimeField(blank=True, null=True, verbose_name='Date and time closed')

    description = models.TextField(blank=True)
    resolution = models.TextField(blank=True)

    service = models.CharField(max_length=63, blank=True)
    root_cause = models.CharField(max_length=63, blank=True)

    priority = models.CharField(max_length=100, blank=True)

    raw_resolution = models.TextField(blank=True)

    def customer_code(self):
        return self.customer.code

    customer_code.admin_order_field = 'customer__code'

    def hours(self):
        try:
            if self.solved_on and self.created_on:
                diff = (self.solved_on - self.created_on)
                diff = diff.total_seconds() / (60 * 60)
                return '%.2f' % diff
            else:
                return '-'
        except:
            log.exception('Unknown error:')
            return '-'


class rRequest(Request):
    class Meta:
        proxy = True
        verbose_name = Request._meta.verbose_name
        verbose_name_plural = Request._meta.verbose_name_plural

        default_permissions = ()
        permissions = (
            ('change_rrequest', 'Can view request only'),
        )


def update_filename(instance, filename):
    newfilename = 'eoh_marval_IMPORT%s%02d.xlsx' % (instance.period.year, instance.period.month)
    return os.path.join('marval', newfilename)


class MarvalImport(models.Model):
    period = models.OneToOneField(Period)
    synced_on = models.DateTimeField(null=True, editable=False)
    result = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to=update_filename)

    def do_sync(self):
        from .utils import marval_sync as ms
        log.info(self.file)

        try:
            df = ms.read_data(year=self.period.year, month=self.period.month)
            df = ms.clean_data(df)
            df = ms.remove_duplicates(df)
            ms.sync_marval(df)

            if df.shape[0] == 0:
                message = 'No new requests for %s-%02d found' % (
                    self.period.year,
                    self.period.month)
                log.info(message)
            else:
                message = 'Successfully sync %s requests for %s-%02d' % (
                    df.shape[0],
                    self.period.year,
                    self.period.month)
                log.info(message)

        except ms.MarvelDataNotFound:
            message = 'Sync failed... %s could not be parsed' % self.file
            log.exception(message)

        return message


# PROXY MODELS
# ---------------------------------------------------------------------------------------------------------------------#
class PortalUser(User):
    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = User._meta.verbose_name
        verbose_name_plural = User._meta.verbose_name_plural


class PortalGroup(Group):
    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = Group._meta.verbose_name
        verbose_name_plural = Group._meta.verbose_name_plural


class PortalPermission(Permission):
    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = Permission._meta.verbose_name
        verbose_name_plural = Permission._meta.verbose_name_plural