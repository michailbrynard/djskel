# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_auto_20140713_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicmodel',
            name='htmlfield',
            field=tinymce.models.HTMLField(default=''),
            preserve_default=False,
        ),
    ]
