# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_myuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advancedmodel',
            name='fkbasic2',
        ),
        migrations.AlterField(
            model_name='advancedmodel',
            name='fkbasic',
            field=models.ForeignKey(to='app1.BasicModel', verbose_name='Basic Foreignkey Filtered', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='advancedmodel',
            name='many2many',
            field=models.ManyToManyField(to='app1.BasicModel', verbose_name='Many 2 Many Relation'),
        ),
    ]
