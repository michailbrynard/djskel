# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app1', '0003_proxyuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProxyUser',
        ),
    ]
