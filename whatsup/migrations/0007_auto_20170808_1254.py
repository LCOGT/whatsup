# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsup', '0006_auto_20160318_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='exposure',
        ),
        migrations.RemoveField(
            model_name='target',
            name='filters',
        ),
        migrations.AlterField(
            model_name='params',
            name='aperture',
            field=models.CharField(default=b'1m0', max_length=3, choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'0m4', b'0.4-meter'), (b'any', b'Any'), (b'sml', b' 1m and 0.4m only')]),
        ),
    ]
