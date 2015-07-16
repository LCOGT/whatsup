# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whatsup', '0001_initial'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='target',
            name='filters',
            field=models.TextField(default=b'rp,v,b', verbose_name=b'filters using approved LCOGT nomenclature, comma separated'),
        ),
        migrations.AddField(
            model_name='target',
            name='project',
            field=models.ForeignKey(blank=True, to='whatsup.Project', null=True),
        ),
    ]
