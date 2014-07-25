# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_basicmodel_htmlfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('name', models.CharField(max_length='20')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('name', models.CharField(max_length='20')),
                ('age', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(to='app1.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='employer',
            field=models.ForeignKey(to='app1.Company'),
            preserve_default=True,
        ),
    ]
