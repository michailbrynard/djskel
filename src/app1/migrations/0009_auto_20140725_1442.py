# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20140725_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='employer',
            field=models.ForeignKey(blank=True, to='app1.Company', null=True),
        ),
    ]
