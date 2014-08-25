# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('description', models.CharField(max_length=45)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BasicModel',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('slug', models.SlugField()),
                ('charfield', models.CharField(blank=True, max_length=50)),
                ('integerfield', models.IntegerField()),
                ('booleanfield', models.BooleanField(default=False)),
                ('choicefield',
                 models.CharField(choices=[('O1', 'Option One'), ('O2', 'Option Two')], default='O1', max_length=3)),
                ('decimalfield', models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)),
                ('datefield', models.DateField(null=True, blank=True)),
                ('emailfield', models.EmailField(blank=True, max_length=75)),
                ('urlfield', models.URLField(null=True, blank=True)),
                ('imagefield', models.ImageField(null=True, blank=True, upload_to='images')),
            ],
            options={
                'ordering': ['charfield'],
                'verbose_name_plural': 'Basic Models',
                'verbose_name': 'Basic Model',
                'permissions': (('permission_code', 'Human readable permission name'),),
                'get_latest_by': 'order_date',
                'default_permissions': ('add', 'change', 'delete'),
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='advancedmodel',
            name='many2many',
            field=models.ManyToManyField(to='app1.BasicModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedmodel',
            name='fkbasic2',
            field=models.ForeignKey(blank=True, null=True, to='app1.BasicModel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedmodel',
            name='fkbasic',
            field=models.ForeignKey(to='app1.BasicModel'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='basicmodel',
            unique_together=set([('emailfield', 'charfield')]),
        ),
        migrations.CreateModel(
            name='ChildModel',
            fields=[
                ('additionalfield', models.CharField(max_length=45)),
                ('basicmodel_ptr',
                 models.OneToOneField(serialize=False, auto_created=True, to='app1.BasicModel', primary_key=True)),
                ('fkadvanced', models.ForeignKey(to='app1.AdvancedModel')),
            ],
            options={
            },
            bases=('app1.basicmodel',),
        ),
    ]
