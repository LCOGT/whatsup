# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constellation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('shortname', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'Constellation',
                'verbose_name_plural': 'Constellations',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('shortname', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(null=True, blank=True)),
                ('ra', models.FloatField(default=0.0, db_index=True)),
                ('dec', models.FloatField(default=0.0)),
                ('avm_code', models.CharField(max_length=50, null=True, blank=True)),
                ('avm_desc', models.CharField(max_length=50, null=True, blank=True)),
                ('exposure', models.TextField(default=b'0', verbose_name=b'default exposure time in RVB')),
                ('filters', models.TextField(default=b'r,v,b', verbose_name=b'filters using approved LCOGT nomenclature, comma separated')),
                ('best', models.BooleanField(default=False, verbose_name=b"Editor's pick")),
                ('aperture', models.CharField(default=b'any', max_length=3, choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'04m', b'0.4-meter'), (b'any', b'Any')])),
                ('constellation', models.ForeignKey(blank=True, to='whatsup.Constellation', null=True)),
                ('project', models.ForeignKey(blank=True, to='whatsup.Project', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Target',
                'verbose_name_plural': 'Targets',
            },
        ),
    ]
