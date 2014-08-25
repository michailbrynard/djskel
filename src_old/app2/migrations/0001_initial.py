# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '__first__'),
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyModel',
            fields=[
            ],
            options={
                'permissions': (('view_basicmodel', 'Can view Basic Model'),),
                'default_permissions': (),
                'verbose_name': 'Basic Model',
                'proxy': True,
                'verbose_name_plural': 'Basic Models',
            },
            bases=('app1.basicmodel',),
        ),
        migrations.CreateModel(
            name='ProxyUser',
            fields=[
            ],
            options={
                'verbose_name': 'User',
                'proxy': True,
                'verbose_name_plural': 'Users',
            },
            bases=('auth.user',),
        ),
    ]
