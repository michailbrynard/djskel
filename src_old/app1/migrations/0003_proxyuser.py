# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '__first__'),
        ('app1', '0002_auto_20140713_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyUser',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Users',
                'verbose_name': 'User',
            },
            bases=('auth.user',),
        ),
    ]
