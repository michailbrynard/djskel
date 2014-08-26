# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedModel',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('slug', models.SlugField()),
                ('char_field', models.CharField(max_length=50, blank=True)),
                ('integer_field', models.IntegerField()),
                ('boolean_field', models.BooleanField(default=False)),
                ('html_field', ckeditor.fields.RichTextField()),
                ('choice_field', models.CharField(choices=[('O1', 'Option One'), ('O2', 'Option Two')], default='O1', max_length=3)),
                ('decimal_field', models.DecimalField(null=True, max_digits=15, decimal_places=2, blank=True)),
                ('date_field', models.DateField(null=True, blank=True)),
                ('email_field', models.EmailField(max_length=75, blank=True)),
                ('url_field', models.URLField(null=True, blank=True)),
                ('image_field', models.ImageField(null=True, upload_to='images', blank=True)),
            ],
            options={
                'get_latest_by': 'order_date',
                'permissions': (('permission_code', 'Human readable permission name'),),
                'ordering': ['char_field'],
                'verbose_name': 'Basic Model',
                'managed': True,
                'verbose_name_plural': 'Basic Models',
                'default_permissions': ('add', 'change', 'delete'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChildModel',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, to='demo_app.BasicModel', parent_link=True)),
                ('additional_field', models.CharField(max_length=45)),
                ('fk_advanced', models.ForeignKey(to='demo_app.AdvancedModel')),
            ],
            options={
            },
            bases=('demo_app.basicmodel',),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('company', models.ForeignKey(null=True, to='demo_app.Company', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(related_name='comapny_owner', to='demo_app.Person'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='basicmodel',
            unique_together=set([('email_field', 'char_field')]),
        ),
        migrations.AddField(
            model_name='advancedmodel',
            name='fk_basic',
            field=models.ForeignKey(null=True, to='demo_app.BasicModel', verbose_name='Basic Foreignkey Filtered', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='advancedmodel',
            name='many2many',
            field=models.ManyToManyField(verbose_name='Many 2 Many Relation', related_name='related_many', to='demo_app.BasicModel'),
            preserve_default=True,
        ),
    ]
