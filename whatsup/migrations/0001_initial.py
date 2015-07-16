# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(null=True, blank=True)),
                ('ra', models.FloatField(default=0.0, db_index=True)),
                ('dec', models.FloatField(default=0.0)),
                ('avm_code', models.CharField(max_length=50, null=True, blank=True)),
                ('avm_desc', models.CharField(max_length=50, null=True, blank=True)),
                ('exposure', models.TextField(default=b'0', verbose_name=b'exposure time on 2-meters')),
                ('best', models.BooleanField(default=False, verbose_name=b"Editor's pick")),
                ('constellation', models.ForeignKey(blank=True, to='whatsup.Constellation', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Target',
                'verbose_name_plural': 'Targets',
            },
        ),
    ]
