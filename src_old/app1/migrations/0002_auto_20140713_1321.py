# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advancedmodel',
            name='fkbasic',
            field=models.ForeignKey(to='app1.BasicModel', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='advancedmodel',
            name='fkbasic2',
            field=models.ForeignKey(to='app1.BasicModel'),
        ),
    ]
