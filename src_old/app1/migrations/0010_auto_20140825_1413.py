# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20140725_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
